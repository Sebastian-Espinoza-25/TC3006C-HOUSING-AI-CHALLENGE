from . import db
from .models import Client, Vendor, ClientPreferences, VendorHouse

# Helpers
def _assign_model_fields(instance, data, *, exclude=()):
    """
    Assign only keys that exist as mapped columns on the instance's model.
    Excludes any keys in 'exclude'.
    """
    cols = {c.name for c in instance.__table__.columns}
    for k, v in (data or {}).items():
        if k in exclude:
            continue
        if k in cols:
            setattr(instance, k, v)

def _truthy_strings():
    # For vendor_houses.central_air (VARCHAR)
    return {"Y", "Yes", "1", "True", "T", "SI", "SÍ", "ON"}

# Client Service
class ClientService:
    @staticmethod
    def get_all_clients():
        clients = Client.query.all()
        return [c.to_dict() for c in clients]

    @staticmethod
    def get_client_by_id(client_id):
        c = Client.query.get(client_id)
        return c.to_dict() if c else None

    @staticmethod
    def create_client(client_data):
        try:
            c = Client(
                username=client_data['username'],
                email=client_data['email'],
                password=client_data['password']  # TODO: hash in prod
            )
            db.session.add(c)
            db.session.commit()
            return c.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def update_client(client_id, client_data):
        try:
            c = Client.query.get(client_id)
            if not c:
                return None
            _assign_model_fields(c, client_data, exclude=('client_id',))
            db.session.commit()
            return c.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_client(client_id):
        try:
            c = Client.query.get(client_id)
            if not c:
                return False
            db.session.delete(c)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

# Vendor Service

class VendorService:
    @staticmethod
    def get_all_vendors():
        vendors = Vendor.query.all()
        return [v.to_dict() for v in vendors]

    @staticmethod
    def get_vendor_by_id(vendor_id):
        v = Vendor.query.get(vendor_id)
        return v.to_dict() if v else None

    @staticmethod
    def create_vendor(vendor_data):
        try:
            v = Vendor(
                username=vendor_data['username'],
                email=vendor_data['email'],
                password=vendor_data['password']  # TODO: hash in prod
            )
            db.session.add(v)
            db.session.commit()
            return v.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def update_vendor(vendor_id, vendor_data):
        try:
            v = Vendor.query.get(vendor_id)
            if not v:
                return None
            _assign_model_fields(v, vendor_data, exclude=('vendor_id',))
            db.session.commit()
            return v.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_vendor(vendor_id):
        try:
            v = Vendor.query.get(vendor_id)
            if not v:
                return False
            db.session.delete(v)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

# House Service 
class HouseService:
    @staticmethod
    #THIS SHOULD BE ONLY USED AFTER THE PRIZE IS PREDICTED BY THE MODEL
    def create_house(vendor_id, house_data):
        """
        Create a house for a vendor.
        Requires vendor_id and at least: title, sale_price.
        You can pass all other house characteristics in house_data (column names from vendor_houses).
        """
        try:
            h = VendorHouse(vendor_id=vendor_id)
            # required
            h.title = house_data['title']
            h.sale_price = float(house_data['sale_price'])

            # optional — assign everything else that exists on the model
            _assign_model_fields(h, house_data, exclude=('house_id', 'vendor_id', 'title', 'sale_price'))

            db.session.add(h)
            db.session.commit()
            return h.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_house(house_id):
        try:
            h = VendorHouse.query.get(house_id)
            if not h:
                return False
            db.session.delete(h)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

# Preferences Service 
class PreferencesService:
    @staticmethod
    def create_preference(client_id, preferences_data):
        """
        Create preferences for a client (one row).
        If a row already exists for this client, update it instead (simple upsert behavior).
        """
        try:
            p = ClientPreferences.query.filter_by(client_id=client_id).first()
            if not p:
                p = ClientPreferences(client_id=client_id)
                db.session.add(p)

            _assign_model_fields(p, preferences_data, exclude=('preference_id', 'client_id'))
            db.session.commit()
            return p.to_dict()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_preference(client_id):
        try:
            p = ClientPreferences.query.filter_by(client_id=client_id).first()
            if not p:
                return False
            db.session.delete(p)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def find_matching_houses(client_id):
        """
        Match houses against a client's preferences.
        Returns:
        {
          'client': {...},
          'matches': [
              {
                'house': {...},
                'vendor': {
                    ...vendor fields...,
                    'contact_phone': <from house>,
                    'contact_email': <from house>
                }
              },
              ...
          ],
          'preferences_applied': {...} | None
        }
        """
        client = Client.query.get(client_id)
        if not client:
            return {'client': None, 'matches': [], 'preferences_applied': None}

        prefs = ClientPreferences.query.filter_by(client_id=client_id).first()
        if not prefs:
            return {'client': client.to_dict(), 'matches': [], 'preferences_applied': None}

        q = VendorHouse.query.filter(VendorHouse.status == 'available')

        # --- Basic filters (use only what is present) ---
        # Price
        if prefs.min_sale_price is not None:
            q = q.filter(VendorHouse.sale_price >= float(prefs.min_sale_price))
        if prefs.max_sale_price is not None:
            q = q.filter(VendorHouse.sale_price <= float(prefs.max_sale_price))

        # Neighborhood / zoning
        if prefs.preferred_neighborhood:
            q = q.filter(VendorHouse.neighborhood == prefs.preferred_neighborhood)
        if prefs.preferred_ms_zoning:
            q = q.filter(VendorHouse.ms_zoning == prefs.preferred_ms_zoning)

        # Selected exact-string preferences
        exact_string_cols = [
            ('preferred_bldg_type', 'bldg_type'),
            ('preferred_house_style', 'house_style'),
            ('preferred_roof_style', 'roof_style'),
            ('preferred_exterior1st', 'exterior1st'),
            ('preferred_exterior2nd', 'exterior2nd'),
            ('preferred_foundation', 'foundation'),
            ('preferred_condition1', 'condition1'),
            ('preferred_functional', 'functional'),
            ('preferred_fireplace_qu', 'fireplace_qu'),
            ('preferred_garage_type', 'garage_type'),
            ('preferred_garage_finish', 'garage_finish'),
            ('preferred_garage_qual', 'garage_qual'),
            ('preferred_garage_cond', 'garage_cond'),
            ('preferred_paved_drive', 'paved_drive'),
            ('preferred_pool_qc', 'pool_qc'),
            ('preferred_fence', 'fence'),
            ('preferred_misc_feature', 'misc_feature'),
            ('preferred_bsmt_qual', 'bsmt_qual'),
            ('preferred_bsmt_cond', 'bsmt_cond'),
            ('preferred_bsmt_exposure', 'bsmt_exposure'),
            ('preferred_bsmt_fin_type1', 'bsmt_fin_type1'),
            ('preferred_bsmt_fin_type2', 'bsmt_fin_type2'),
            ('preferred_heating_qc', 'heating_qc'),
            ('preferred_electrical', 'electrical'),
        ]
        for pref_attr, house_col in exact_string_cols:
            val = getattr(prefs, pref_attr)
            if val:
                q = q.filter(getattr(VendorHouse, house_col) == val)

        # Central air (bool pref vs VARCHAR column)
        if prefs.central_air_required:
            q = q.filter(VendorHouse.central_air.in_(_truthy_strings()))

        # A few common numeric ranges 
        if prefs.min_bedroom_abv_gr is not None:
            q = q.filter(VendorHouse.bedroom_abv_gr >= float(prefs.min_bedroom_abv_gr))
        if prefs.max_bedroom_abv_gr is not None:
            q = q.filter(VendorHouse.bedroom_abv_gr <= float(prefs.max_bedroom_abv_gr))
        if prefs.min_full_bath is not None:
            q = q.filter(VendorHouse.full_bath >= float(prefs.min_full_bath))
        if prefs.max_full_bath is not None:
            q = q.filter(VendorHouse.full_bath <= float(prefs.max_full_bath))
        if prefs.min_gr_liv_area is not None:
            q = q.filter(VendorHouse.gr_liv_area >= float(prefs.min_gr_liv_area))
        if prefs.max_gr_liv_area is not None:
            q = q.filter(VendorHouse.gr_liv_area <= float(prefs.max_gr_liv_area))

        houses = q.all()

        # Join vendor info for each house and return contact info
        matches = []
        for h in houses:
            v = Vendor.query.get(h.vendor_id)
            vendor_info = v.to_dict() if v else None
            if vendor_info is None:
                continue

            # Add contact info from the house listing to vendor payload
            vendor_info_with_contact = {
                **vendor_info,
                'contact_phone': h.contact_phone,
                'contact_email': h.contact_email,
            }

            matches.append({
                'house': h.to_dict(),
                'vendor': vendor_info_with_contact
            })

        return {
            'client': client.to_dict(),
            'matches': matches,
            'preferences_applied': prefs.to_dict()
        }
