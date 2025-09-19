from datetime import datetime
from . import db

# HELPERS

def _to_dict_all(model):
    """Autoserialer for all columns"""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}

# TABLES

# Client Table
class Client(db.Model):
    """Contains registered clients."""
    __tablename__ = 'clients'

    client_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email     = db.Column(db.String(255), nullable=False, unique=True)
    username  = db.Column(db.String(100), nullable=False, unique=True)
    password  = db.Column(db.String(255), nullable=False)

    # 1:N with client_preferences (schema allows multiple rows per client)
    preferences = db.relationship(
        'ClientPreferences',
        backref='client',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return _to_dict_all(self)


class Vendor(db.Model):
    """Contains registered vendors."""
    __tablename__ = 'vendors'

    vendor_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    email     = db.Column(db.String(255), nullable=False, unique=True)
    username  = db.Column(db.String(100), nullable=False, unique=True)
    password  = db.Column(db.String(255), nullable=False)

    # 1:N with vendor_houses
    houses = db.relationship(
        'VendorHouse',
        backref='vendor',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return _to_dict_all(self)


class ClientPreferences(db.Model):
    """Contains client preferences for houuse matching"""
    __tablename__ = 'client_preferences'

    preference_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    client_id     = db.Column(
        db.BigInteger,
        db.ForeignKey('clients.client_id', ondelete='CASCADE'),
        nullable=False
    )

    # Location and lot preferences
    preferred_neighborhood = db.Column(db.String(100))
    preferred_ms_zoning    = db.Column(db.String(20))
    preferred_lot_shape    = db.Column(db.String(20))
    preferred_land_contour = db.Column(db.String(20))
    preferred_lot_config   = db.Column(db.String(20))
    preferred_condition1   = db.Column(db.String(20))

    # House type and style
    preferred_bldg_type    = db.Column(db.String(20))
    preferred_house_style  = db.Column(db.String(20))
    preferred_roof_style   = db.Column(db.String(20))
    preferred_exterior1st  = db.Column(db.String(20))
    preferred_exterior2nd  = db.Column(db.String(20))
    preferred_foundation   = db.Column(db.String(20))

    # Quality and condition
    min_overall_qual = db.Column(db.Float)
    max_overall_qual = db.Column(db.Float)
    min_overall_cond = db.Column(db.Float)
    max_overall_cond = db.Column(db.Float)
    min_exter_qual   = db.Column(db.String(20))
    min_exter_cond   = db.Column(db.String(20))

    # Years
    min_year_built     = db.Column(db.Integer)
    max_year_built     = db.Column(db.Integer)
    min_year_remod_add = db.Column(db.Integer)
    max_year_remod_add = db.Column(db.Integer)
    min_remod_age      = db.Column(db.Float)
    max_remod_age      = db.Column(db.Float)
    min_house_age      = db.Column(db.Float)
    max_house_age      = db.Column(db.Float)

    # Sizes and areas
    min_lot_area      = db.Column(db.Float)
    max_lot_area      = db.Column(db.Float)
    min_lot_frontage  = db.Column(db.Float)
    max_lot_frontage  = db.Column(db.Float)
    min_1st_flr_sf    = db.Column(db.Float)
    max_1st_flr_sf    = db.Column(db.Float)
    min_2nd_flr_sf    = db.Column(db.Float)
    max_2nd_flr_sf    = db.Column(db.Float)
    min_gr_liv_area   = db.Column(db.Float)
    max_gr_liv_area   = db.Column(db.Float)
    min_total_bsmt_sf = db.Column(db.Float)
    max_total_bsmt_sf = db.Column(db.Float)
    min_total_sf      = db.Column(db.Float)
    max_total_sf      = db.Column(db.Float)

    # Rooms and bathrooms
    min_bedroom_abv_gr  = db.Column(db.Integer)
    max_bedroom_abv_gr  = db.Column(db.Integer)
    min_kitchen_abv_gr  = db.Column(db.Integer)
    max_kitchen_abv_gr  = db.Column(db.Integer)
    min_tot_rms_abv_grd = db.Column(db.Integer)
    max_tot_rms_abv_grd = db.Column(db.Integer)
    min_full_bath       = db.Column(db.Integer)
    max_full_bath       = db.Column(db.Integer)
    min_half_bath       = db.Column(db.Integer)
    max_half_bath       = db.Column(db.Integer)
    min_bsmt_full_bath  = db.Column(db.Integer)
    max_bsmt_full_bath  = db.Column(db.Integer)
    min_bsmt_half_bath  = db.Column(db.Integer)
    max_bsmt_half_bath  = db.Column(db.Integer)
    min_total_bath      = db.Column(db.Float)
    max_total_bath      = db.Column(db.Float)

    # Basement
    preferred_bsmt_qual      = db.Column(db.String(20))
    preferred_bsmt_cond      = db.Column(db.String(20))
    preferred_bsmt_exposure  = db.Column(db.String(20))
    preferred_bsmt_fin_type1 = db.Column(db.String(20))
    preferred_bsmt_fin_type2 = db.Column(db.String(20))
    min_bsmt_fin_sf1         = db.Column(db.Float)
    max_bsmt_fin_sf1         = db.Column(db.Float)
    min_bsmt_fin_sf2         = db.Column(db.Float)
    max_bsmt_fin_sf2         = db.Column(db.Float)
    min_bsmt_unf_sf          = db.Column(db.Float)
    max_bsmt_unf_sf          = db.Column(db.Float)

    # AC/Heating/Electrical
    preferred_heating_qc   = db.Column(db.String(20))
    central_air_required   = db.Column(db.Boolean, default=False)
    preferred_electrical   = db.Column(db.String(20))

    # Kitchen
    min_kitchen_qual       = db.Column(db.String(20))

    # Functionality
    preferred_functional   = db.Column(db.String(20))

    # Chimneys
    min_fireplaces         = db.Column(db.Integer)
    max_fireplaces         = db.Column(db.Integer)
    preferred_fireplace_qu = db.Column(db.String(20))

    # Garage
    preferred_garage_type   = db.Column(db.String(20))
    min_garage_yr_blt       = db.Column(db.Integer)
    max_garage_yr_blt       = db.Column(db.Integer)
    preferred_garage_finish = db.Column(db.String(20))
    min_garage_cars         = db.Column(db.Integer)
    max_garage_cars         = db.Column(db.Integer)
    min_garage_area         = db.Column(db.Float)
    max_garage_area         = db.Column(db.Float)
    preferred_garage_qual   = db.Column(db.String(20))
    preferred_garage_cond   = db.Column(db.String(20))
    preferred_paved_drive   = db.Column(db.String(20))
    min_garage_score        = db.Column(db.Float)
    max_garage_score        = db.Column(db.Float)

    # Exterior
    min_wood_deck_sf  = db.Column(db.Float)
    max_wood_deck_sf  = db.Column(db.Float)
    min_open_porch_sf = db.Column(db.Float)
    max_open_porch_sf = db.Column(db.Float)
    min_enclosed_porch = db.Column(db.Float)
    max_enclosed_porch = db.Column(db.Float)
    min_3ssn_porch    = db.Column(db.Float)
    max_3ssn_porch    = db.Column(db.Float)
    min_screen_porch  = db.Column(db.Float)
    max_screen_porch  = db.Column(db.Float)
    min_total_porch_sf = db.Column(db.Float)
    max_total_porch_sf = db.Column(db.Float)
    min_rooms_plus_bath_eq = db.Column(db.Float)
    max_rooms_plus_bath_eq = db.Column(db.Float)

    # Pool
    min_pool_area = db.Column(db.Float)
    max_pool_area = db.Column(db.Float)
    preferred_pool_qc = db.Column(db.String(20))

    # Fences/Misc
    preferred_fence        = db.Column(db.String(20))
    preferred_misc_feature = db.Column(db.String(20))

    # Price
    min_sale_price = db.Column(db.Float)
    max_sale_price = db.Column(db.Float)

    # Sale info
    preferred_sale_type      = db.Column(db.String(20))
    preferred_sale_condition = db.Column(db.String(20))

    #New columns

    min_remod_age = db.Column(db.Float)
    max_remod_age = db.Column(db.Float)
    min_house_age = db.Column(db.Float)
    max_house_age = db.Column(db.Float)
    min_total_porch_sf = db.Column(db.Float)
    max_total_porch_sf = db.Column(db.Float)
    min_rooms_plus_bath_eq = db.Column(db.Float)
    max_rooms_plus_bath_eq = db.Column(db.Float)
    min_total_bath = db.Column(db.Float)
    max_total_bath = db.Column(db.Float)
    min_total_sf = db.Column(db.Float)
    max_total_sf = db.Column(db.Float)
    min_garage_score = db.Column(db.Float)
    max_garage_score = db.Column(db.Float)

    def to_dict(self):
        return _to_dict_all(self)


class VendorHouse(db.Model):
    """Contains house characteristics and details for sale by vendors."""
    __tablename__ = 'vendor_houses'

    house_id  = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    vendor_id = db.Column(
        db.BigInteger,
        db.ForeignKey('vendors.vendor_id', ondelete='CASCADE'),
        nullable=False
    )

    # Basic info
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    sale_price  = db.Column(db.Float, nullable=False)

    # Classification
    ms_sub_class = db.Column(db.Float)
    ms_zoning    = db.Column(db.String(20))

    # Lot
    lot_frontage  = db.Column(db.Float)
    lot_area      = db.Column(db.Float)
    alley         = db.Column(db.String(20))
    lot_shape     = db.Column(db.String(20))
    land_contour  = db.Column(db.String(20))
    lot_config    = db.Column(db.String(20))
    neighborhood  = db.Column(db.String(100))
    condition1    = db.Column(db.String(20))

    # Type and style
    bldg_type   = db.Column(db.String(20))
    house_style = db.Column(db.String(20))

    # Quality and condition
    overall_qual = db.Column(db.Float)
    overall_cond = db.Column(db.Float)

    # Years
    year_built     = db.Column(db.Float)
    year_remod_add = db.Column(db.Float)
    remod_age      = db.Column(db.Float)
    house_age      = db.Column(db.Float)

    # Roof
    roof_style = db.Column(db.String(20))

    # Exterior
    exterior1st  = db.Column(db.String(20))
    exterior2nd  = db.Column(db.String(20))
    mas_vnr_type = db.Column(db.String(20))
    mas_vnr_area = db.Column(db.Float)
    exter_qual   = db.Column(db.String(20))
    exter_cond   = db.Column(db.String(20))

    # Foundation
    foundation = db.Column(db.String(20))

    # Basement
    bsmt_qual      = db.Column(db.String(20))
    bsmt_cond      = db.Column(db.String(20))
    bsmt_exposure  = db.Column(db.String(20))
    bsmt_fin_type1 = db.Column(db.String(20))
    bsmt_fin_sf1   = db.Column(db.Float)
    bsmt_fin_type2 = db.Column(db.String(20))
    bsmt_fin_sf2   = db.Column(db.Float)
    bsmt_unf_sf    = db.Column(db.Float)
    total_bsmt_sf  = db.Column(db.Float)

    # AC/Heating/Electrical
    heating_qc   = db.Column(db.String(20))
    central_air  = db.Column(db.String(20))  # VARCHAR(20) in schema (not boolean)
    electrical   = db.Column(db.String(20))

    # Sizes and areas
    first_flr_sf  = db.Column(db.Float)
    second_flr_sf = db.Column(db.Float)
    gr_liv_area   = db.Column(db.Float)
    total_sf      = db.Column(db.Float)

    # Bathrooms
    bsmt_full_bath = db.Column(db.Float)
    bsmt_half_bath = db.Column(db.Float)
    full_bath      = db.Column(db.Float)
    half_bath      = db.Column(db.Float)
    total_bath     = db.Column(db.Float)

    # Rooms
    bedroom_abv_gr  = db.Column(db.Float)
    kitchen_abv_gr  = db.Column(db.Float)
    kitchen_qual    = db.Column(db.String(20))
    tot_rms_abv_grd = db.Column(db.Float)
    rooms_plus_bath_eq = db.Column(db.Float)

    # Functionality
    functional = db.Column(db.String(20))

    # Chimneys
    fireplaces   = db.Column(db.Float)
    fireplace_qu = db.Column(db.String(20))

    # Garage
    garage_type   = db.Column(db.String(20))
    garage_yr_blt = db.Column(db.Float)
    garage_finish = db.Column(db.String(20))
    garage_cars   = db.Column(db.Float)
    garage_area   = db.Column(db.Float)
    garage_qual   = db.Column(db.String(20))
    garage_cond   = db.Column(db.String(20))
    paved_drive   = db.Column(db.String(20))
    garage_score  = db.Column(db.Float)

    # Exterior features
    wood_deck_sf    = db.Column(db.Float)
    open_porch_sf   = db.Column(db.Float)
    enclosed_porch  = db.Column(db.Float)
    three_ssn_porch = db.Column(db.Float)
    screen_porch    = db.Column(db.Float)
    total_porch_sf  = db.Column(db.Float)

    # Pool
    pool_area = db.Column(db.Float)
    pool_qc   = db.Column(db.String(20))

    # Fences/Misc
    fence        = db.Column(db.String(20))
    misc_feature = db.Column(db.String(20))

    # Sale info
    mo_sold        = db.Column(db.Float)
    yr_sold        = db.Column(db.Float)
    sale_type      = db.Column(db.String(20))
    sale_condition = db.Column(db.String(20))

    # Satus 
    status      = db.Column(db.String(20), default='available')
    is_featured = db.Column(db.Boolean, default=False)

    # Contact
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(255))

    #New columns
    total_porch_sf = db.Column(db.Float)
    rooms_plus_bath_eq = db.Column(db.Float)
    total_bath = db.Column(db.Float)
    total_sf = db.Column(db.Float)
    remod_age = db.Column(db.Float)
    house_age = db.Column(db.Float)
    garage_score = db.Column(db.Float)

    def to_dict(self):
        return _to_dict_all(self)
