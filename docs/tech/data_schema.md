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

### wards
Ward boundaries and identifiers.

| Column Name   | Data Type | Description                                 |
|---------------|-----------|---------------------------------------------|
| id            | integer   | Unique identifier                           |
| name          | text      | Name of the ward                            |
| ward_id       | integer   | Ward ID for linking to other tables         |
| geometry      | geometry  | Geometry: polygon boundary of the ward      |