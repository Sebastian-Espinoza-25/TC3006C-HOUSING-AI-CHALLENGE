Schema for HouseLink Database
CREATE DATABASE houselink;

-- 1) Clients
CREATE TABLE clients (
    client_id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    email          VARCHAR(255) NOT NULL UNIQUE,
    username       VARCHAR(100) NOT NULL UNIQUE,
    password       VARCHAR(255) NOT NULL
);

-- 2) Vendors
CREATE TABLE vendors (
    vendor_id      BIGINT AUTO_INCREMENT PRIMARY KEY,
    email          VARCHAR(255) NOT NULL UNIQUE,
    username       VARCHAR(100) NOT NULL UNIQUE,
    password       VARCHAR(255) NOT NULL
);

-- 3) Client Preferences
-- Each column is a preference related to a house characteristic.
CREATE TABLE client_preferences (
    preference_id  BIGINT AUTO_INCREMENT PRIMARY KEY,
    client_id      BIGINT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
    
    -- Preferencias de ubicación y zona
    preferred_neighborhood VARCHAR(100),
    preferred_ms_zoning VARCHAR(20),
    preferred_lot_shape VARCHAR(20),
    preferred_land_contour VARCHAR(20),
    preferred_lot_config VARCHAR(20),
    preferred_condition1 VARCHAR(20),
    
    -- Preferencias de tipo de casa
    preferred_bldg_type VARCHAR(20),
    preferred_house_style VARCHAR(20),
    preferred_roof_style VARCHAR(20),
    preferred_exterior1st VARCHAR(20),
    preferred_exterior2nd VARCHAR(20),
    preferred_foundation VARCHAR(20),
    
    -- Preferencias de calidad y condición
    min_overall_qual FLOAT,
    max_overall_qual FLOAT,
    min_overall_cond FLOAT,
    max_overall_cond FLOAT,
    min_exter_qual VARCHAR(20),
    min_exter_cond VARCHAR(20),
    
    -- Preferencias de año de construcción
    min_year_built INT,
    max_year_built INT,
    min_year_remod_add INT,
    max_year_remod_add INT,
    min_remod_age FLOAT,
    max_remod_age FLOAT,
    min_house_age FLOAT,
    max_house_age FLOAT,
    
    -- Preferencias de tamaño y área
    min_lot_area FLOAT,
    max_lot_area FLOAT,
    min_lot_frontage FLOAT,
    max_lot_frontage FLOAT,
    min_1st_flr_sf FLOAT,
    max_1st_flr_sf FLOAT,
    min_2nd_flr_sf FLOAT,
    max_2nd_flr_sf FLOAT,
    min_gr_liv_area FLOAT,
    max_gr_liv_area FLOAT,
    min_total_bsmt_sf FLOAT,
    max_total_bsmt_sf FLOAT,
    min_total_sf FLOAT,
    max_total_sf FLOAT,
    
    -- Preferencias de habitaciones y baños
    min_bedroom_abv_gr INT,
    max_bedroom_abv_gr INT,
    min_kitchen_abv_gr INT,
    max_kitchen_abv_gr INT,
    min_tot_rms_abv_grd INT,
    max_tot_rms_abv_grd INT,
    min_full_bath INT,
    max_full_bath INT,
    min_half_bath INT,
    max_half_bath INT,
    min_bsmt_full_bath INT,
    max_bsmt_full_bath INT,
    min_bsmt_half_bath INT,
    max_bsmt_half_bath INT,
    min_total_bath FLOAT,
    max_total_bath FLOAT,
    
    -- Preferencias de sótano
    preferred_bsmt_qual VARCHAR(20),
    preferred_bsmt_cond VARCHAR(20),
    preferred_bsmt_exposure VARCHAR(20),
    preferred_bsmt_fin_type1 VARCHAR(20),
    preferred_bsmt_fin_type2 VARCHAR(20),
    min_bsmt_fin_sf1 FLOAT,
    max_bsmt_fin_sf1 FLOAT,
    min_bsmt_fin_sf2 FLOAT,
    max_bsmt_fin_sf2 FLOAT,
    min_bsmt_unf_sf FLOAT,
    max_bsmt_unf_sf FLOAT,
    
    -- Preferencias de calefacción y aire acondicionado
    preferred_heating_qc VARCHAR(20),
    central_air_required BOOLEAN DEFAULT FALSE,
    preferred_electrical VARCHAR(20),
    
    -- Preferencias de cocina
    min_kitchen_qual VARCHAR(20),
    
    -- Preferencias de funcionalidad
    preferred_functional VARCHAR(20),
    
    -- Preferencias de chimeneas
    min_fireplaces INT,
    max_fireplaces INT,
    preferred_fireplace_qu VARCHAR(20),
    
    -- Preferencias de garaje
    preferred_garage_type VARCHAR(20),
    min_garage_yr_blt INT,
    max_garage_yr_blt INT,
    preferred_garage_finish VARCHAR(20),
    min_garage_cars INT,
    max_garage_cars INT,
    min_garage_area FLOAT,
    max_garage_area FLOAT,
    preferred_garage_qual VARCHAR(20),
    preferred_garage_cond VARCHAR(20),
    preferred_paved_drive VARCHAR(20),
    min_garage_score FLOAT,
    max_garage_score FLOAT,
    
    -- Preferencias de porches y exteriores
    min_wood_deck_sf FLOAT,
    max_wood_deck_sf FLOAT,
    min_open_porch_sf FLOAT,
    max_open_porch_sf FLOAT,
    min_enclosed_porch FLOAT,
    max_enclosed_porch FLOAT,
    min_3ssn_porch FLOAT,
    max_3ssn_porch FLOAT,
    min_screen_porch FLOAT,
    max_screen_porch FLOAT,
    min_total_porch_sf FLOAT,
    max_total_porch_sf FLOAT,
    min_rooms_plus_bath_eq FLOAT,
    max_rooms_plus_bath_eq FLOAT,
    
    -- Preferencias de piscina
    min_pool_area FLOAT,
    max_pool_area FLOAT,
    preferred_pool_qc VARCHAR(20),
    
    -- Preferencias de cercas y características misceláneas
    preferred_fence VARCHAR(20),
    preferred_misc_feature VARCHAR(20),
    
    -- Preferencias de precio
    min_sale_price FLOAT,
    max_sale_price FLOAT,
    
    -- Preferencias de tipo de venta
    preferred_sale_type VARCHAR(20),
    preferred_sale_condition VARCHAR(20)
);

-- 4) Vendor Houses
-- Each column is a characteristic of the house.
CREATE TABLE vendor_houses (
    house_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    vendor_id      BIGINT NOT NULL,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id) ON DELETE CASCADE,
    
    -- Información básica de la casa
    title          VARCHAR(200) NOT NULL,
    description    TEXT,
    sale_price     FLOAT NOT NULL,
    
    -- Clasificación de la casa
    ms_sub_class   FLOAT,
    ms_zoning      VARCHAR(20),
    
    -- Información del lote
    lot_frontage   FLOAT,
    lot_area       FLOAT,
    alley          VARCHAR(20),
    lot_shape      VARCHAR(20),
    land_contour   VARCHAR(20),
    lot_config     VARCHAR(20),
    neighborhood   VARCHAR(100),
    condition1     VARCHAR(20),
    
    -- Tipo y estilo de construcción
    bldg_type      VARCHAR(20),
    house_style    VARCHAR(20),
    
    -- Calidad y condición general
    overall_qual   FLOAT,
    overall_cond   FLOAT,
    
    -- Años de construcción y remodelación
    year_built     FLOAT,
    year_remod_add FLOAT,
    remod_age      FLOAT,
    house_age      FLOAT,
    
    -- Características del techo
    roof_style     VARCHAR(20),
    
    -- Exteriores
    exterior1st    VARCHAR(20),
    exterior2nd    VARCHAR(20),
    mas_vnr_type   VARCHAR(20),
    mas_vnr_area   FLOAT,
    exter_qual     VARCHAR(20),
    exter_cond     VARCHAR(20),
    
    -- Fundación
    foundation     VARCHAR(20),
    
    -- Sótano
    bsmt_qual      VARCHAR(20),
    bsmt_cond      VARCHAR(20),
    bsmt_exposure  VARCHAR(20),
    bsmt_fin_type1 VARCHAR(20),
    bsmt_fin_sf1   FLOAT,
    bsmt_fin_type2 VARCHAR(20),
    bsmt_fin_sf2   FLOAT,
    bsmt_unf_sf    FLOAT,
    total_bsmt_sf  FLOAT,
    
    -- Calefacción y aire acondicionado
    heating_qc     VARCHAR(20),
    central_air    VARCHAR(20),
    electrical     VARCHAR(20),
    
    -- Áreas de piso
    first_flr_sf   FLOAT,
    second_flr_sf  FLOAT,
    gr_liv_area    FLOAT,
    total_sf       FLOAT,
    
    -- Baños
    bsmt_full_bath FLOAT,
    bsmt_half_bath FLOAT,
    full_bath      FLOAT,
    half_bath      FLOAT,
    total_bath     FLOAT,
    
    -- Habitaciones
    bedroom_abv_gr FLOAT,
    kitchen_abv_gr FLOAT,
    kitchen_qual   VARCHAR(20),
    tot_rms_abv_grd FLOAT,
    rooms_plus_bath_eq FLOAT,
    
    -- Funcionalidad
    functional     VARCHAR(20),
    
    -- Chimeneas
    fireplaces     FLOAT,
    fireplace_qu   VARCHAR(20),
    
    -- Garaje
    garage_type    VARCHAR(20),
    garage_yr_blt  FLOAT,
    garage_finish  VARCHAR(20),
    garage_cars    FLOAT,
    garage_area    FLOAT,
    garage_qual    VARCHAR(20),
    garage_cond    VARCHAR(20),
    paved_drive    VARCHAR(20),
    garage_score   FLOAT,
    
    -- Porches y exteriores
    wood_deck_sf   FLOAT,
    open_porch_sf  FLOAT,
    enclosed_porch FLOAT,
    three_ssn_porch FLOAT,
    screen_porch   FLOAT,
    total_porch_sf FLOAT,
    
    -- Piscina
    pool_area      FLOAT,
    pool_qc        VARCHAR(20),
    
    -- Cercas y características misceláneas
    fence          VARCHAR(20),
    misc_feature   VARCHAR(20),
    
    -- Información de venta
    mo_sold        FLOAT,
    yr_sold        FLOAT,
    sale_type      VARCHAR(20),
    sale_condition VARCHAR(20),
    
    -- Estado de la casa
    status         VARCHAR(20) DEFAULT 'available',
    is_featured    BOOLEAN DEFAULT FALSE,
    
    -- Información de contacto
    contact_phone  VARCHAR(20),
    contact_email  VARCHAR(255)
);
