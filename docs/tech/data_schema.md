# Data Schema
**Purpose: This document describes all tables in the Geoff system, including metadata and transformed/processed datasets.**
---

## Data Dictionary

### ambulance_stations
Ambulance stations in the city, including address, EMS info, and location.

| Column Name   | Data Type | Description                                 |
|---------------|-----------|---------------------------------------------|
| id            | integer   | Unique identifier                           |
| address       | text      | Street address of the station               |
| municipality  | text      | Municipality of the station                 |
| name          | text      | Name of the station                         |
| ems_id        | integer   | EMS ID                                      |
| ems_name      | text      | EMS short name of the station               |
| ems_website   | text      | Website of ambulance station                |
| geometry      | geometry  | Geometry: point location of the station     |

### attractions
Attractions and points of interest, including name, category, contact, and location.

| Column Name   | Data Type | Description                                      |
|---------------|-----------|--------------------------------------------------|
| id            | integer   | Unique identifier                                |
| name          | text      | Name of the attraction or point of interest      |
| category      | text      | Category or type that the attraction is          |
| phone         | text      | Business phone number if available               |
| website       | text      | Business website if available                    |
| address       | text      | Street address of attraction                     |
| municipality  | text      | Municipality of the attraction                   |
| centreline    | integer   | ID key for Centreline table                      |
| ward          | text      | Name of Ward attraction is in                    |
| ward_id       | integer   | ID of Ward attraction is in                      |
| description   | text      | Description of the attraction or point of interest|
| geometry      | geometry  | Geometry: point location of the attraction       |

### bike_lanes
Bike lane segments, including installation year, street info, and geometry.

| Column Name     | Data Type | Description                                         |
|-----------------|-----------|-----------------------------------------------------|
| id              | integer   | Unique identifier                                   |
| installed_year  | integer   | Year the bike lane was first installed              |
| upgraded_year   | integer   | Year the bike lane was last upgraded                |
| street_name     | text      | Primary street name where the bike lane is located  |
| from_street     | text      | Cross street marking start of the bike lane         |
| to_street       | text      | Cross street marking the end of the bike lane       |
| lane_type       | text      | Type of infrastructure (e.g Sharrows, multi-use trail)|
| converted       | text      | Year the bike lane was converted                    |
| geometry        | geometry  | Geometry: line segment of the bike lane             |

### building_outlines
Building footprints and outlines, including building type, height, and elevation data.

Column Name           | Data Type | Description                                                                  |
|-----------------------|-----------|------------------------------------------------------------------------------|
id                    | integer   | Unique identifier                                                            |
subtype_desc          | text      | Text description of outline subtype: "Miscellaneous Structure", "Building Outline", or "Garage" |
subtype_code          | integer   | Short code categorizing outline subtype                                      |
elevation             | integer   | Ground elevation of the feature (meters)                                     |
derived_height        | integer   | Height of the feature derived from LiDAR data (meters)                       |
objectid              | integer   | Unique object ID of the feature                                              |
last_attribute_maint  | text      | Date of the last attribute edit                                              |
last_geometry_maint   | text      | Date of last geometry edit                                                   |
geometry              | geometry  | Geometry: polygon location of the building                                   |

### fire_stations
Fire stations, including address, municipality, station number, and location.

| Column Name   | Data Type | Description                                 |
|---------------|-----------|---------------------------------------------|
| id            | integer   | Unique identifier                           |
| address       | text      | Street address of fire stations             |
| municipality  | text      | Municipality of the station                 |
| station_no    | integer   | FD number of the station                    |
| year_built    | integer   | Year the station was built                  |
| type          | text      | Fire station or operaitons centre           |
| geometry      | geometry  | Geometry: point location of the fire station|

### neighbourhoods
Neighbourhood boundaries and classification.

| Column Name         | Data Type | Description                                         |
|---------------------|-----------|-----------------------------------------------------|
| id                  | integer   | Unique identifier                                   |
| area_name           | text      | Official neighbourhood name                         |
| classification      | text      | Classification tag for improvement or emerging type |
| classification_code | text      | Classification title for improvement or emerging type|
| geometry            | geometry  | Geometry: boundary polygon of the neighbourhood     |

### parking_lots
Parking lot boundaries and last update date.

| Column Name   | Data Type | Description                                 |
|---------------|-----------|---------------------------------------------|
| id            | integer   | Unique identifier                           |
| last_updated  | text      | Data of last change to lot data             |
| geometry      | geometry  | Geometry: boundary polygon of the parking lot|

### parks
Parks, including name, type, amenities, and location.

| Column Name   | Data Type | Description                                 |
|---------------|-----------|---------------------------------------------|
| id            | integer   | Unique identifier                           |
| name          | text      | Official park name                          |
| type          | text      | Category of park                            |
| amenities     | text      | List of amenities in the park               |
| geometry      | geometry  | Geometry: point location of the park        |

### police_stations
Police stations, including name, address, and location.

| Column Name   | Data Type | Description                                 |
|---------------|-----------|---------------------------------------------|
| id            | integer   | Unique identifier                           |
| name          | text      | Name of the station                         |
| address       | text      | Street address pf tje station               |
| geometry      | geometry  | Geometry: point location of the station     |

### schools
Schools, including name, type, board, address, and location.

| Column Name       | Data Type | Description                                 |
|-------------------|-----------|---------------------------------------------|
| id                | integer   | Unique identifier                           |
| name              | text      | Name of the school                          |
| school_type       | text      | Short code for type (FP - French Public, FS - French Separate, EP - English Public, ES - English Separate, PR - Private)|
| school_type_desc  | text      | Long form of type                           |
| school_board_name | text      | School board name                           |
| address           | text      | Street address                              |
| geometry          | geometry  | Geometry: point location of the school      |

### transit_stops
Transit stop locations from GTFS data, including accessibility information.

Column Name         | Data Type | Description                                         |
|---------------------|-----------|-----------------------------------------------------|
id                  | integer   | Unique identifier (stop_id from GTFS)               |
name                | text      | Name of the transit stop                            |
description         | integer   | Description code of the stop                        |
wheelchair_boarding | integer   | Whether there is accessible boarding at the stop (0=unknown, 1=accessible, 2=not accessible) |
location_type       | integer   | Location type of the stop (0=stop, 1=station)       |
geometry            | geometry  | Geometry: point location of the stop                |

### wards
Ward boundaries and identifiers.

| Column Name   | Data Type | Description                                 |
|---------------|-----------|---------------------------------------------|
| id            | integer   | Unique identifier                           |
| name          | text      | Name of the ward                            |
| ward_id       | integer   | Ward ID for linking to other tables         |
| geometry      | geometry  | Geometry: polygon boundary of the ward      |

### zoning
Zoning designations and regulations, including zone types, dwelling unit limits, and exceptions.

Column Name       | Data Type | Description                                                                                                                                                                                                                                                                                                            |
|-------------------|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
id                | integer   | Unique identifier                                                                                                                                                                                                                                                                                                      |
zone              | text      | Name of the zone. R: Residential, RD: Residential Detached, RS: Residential Semi-Detached, RM: Residential Multiple, RA: Residential Apartment, RAC: Residential Apartment Commercial, O: Open Space, ON: Open Space Natural, OR: Open Space Recreation, UT: Utility & Transport, CL: Commercial Local, CR: Commercial Residential, CRE: Commercial Residential Employment, EL: Employment Light Industrial, E: Employment Industrial, EH: Employment Heavy Industrial, EO: Employment Office, I: Institutional, IH: Institutional Hospital, IE: Institutional Education, IS: Institutional School |
zone_code         | integer   | Numeric code for zone category. 0=Residential, 1=Open Space, 2=Utility and Transportation, 4=Employment Industrial, 5=Institutional, 6=Commercial Residential Employment, 101=Residential Apartment, 201=Commercial, 202=Commercial Residential |
max_units         | integer   | The permitted maximum number of dwelling units allowed on a lot in the zone. -1 indicates no specific limit                                                                                                                                                                                                           |
full_zone_string  | text      | Complete label of the zone including all modifiers                                                                                                                                                                                                                                                                     |
zoning_exception  | text      | Indicates whether a zone has an exception (Y=Yes, N=No, NULL=unknown)                                                                                                                                                                                                                                                 |
geometry          | geometry  | Geometry: polygon location of the zone                                                                                                                                                                                                                                                                                 |