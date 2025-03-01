from flask import Flask, request, jsonify, render_template
import pandas as pd
from shapely.geometry import Point
from shapely.wkt import loads
from geopy.geocoders import Nominatim
import geopandas as gpd
import folium


app = Flask(__name__)

# Load the neighborhood data
data = pd.read_csv("Census_2006_-_Neighbourhood_Boundary_20250127.csv")
data["geometry"] = data["the_geom"].apply(loads)
neighborhoods = gpd.GeoDataFrame(data, geometry="geometry", crs="EPSG:4326")

# Comprehensive Mapping of Neighborhoods to CMHC Zones
neighborhood_to_cmhc = {
    # Fort Rouge area
    "Crescentwood": "Fort Rouge",
    "Lord Roberts": "Fort Rouge",
    "Roslyn": "Fort Rouge",
    "Armstrong Point": "Fort Rouge",
    "River-Osborne": "Fort Rouge",
    "Grant Park": "Fort Rouge",
    "Riverview": "Fort Rouge",
    "Wildwood": "Fort Rouge",
    "Wellington Crescent": "Fort Rouge",
    "Ebby-wentworth": "Fort Rouge",

    # St. Vital area
    "Pulberry": "St. Vital",
    "Norberry": "St. Vital",
    "Varennes": "St. Vital",
    "Minnetonka": "St. Vital",
    "Worthington": "St. Vital",
    "Meadowood": "St. Vital",
    "Victoria Crescent": "St. Vital",
    "Dakota Crossing": "St. Vital",
    "River Park South": "St. Vital",
    "Island Lakes": "St. Vital",
    "Southdale": "St. Vital",
    "Royalwood": "St. Vital",
    "Niakwa Park": "St. Vital",
    "Windsor Park": "St. Vital",

    # Assiniboine Park area
    "Assiniboine Park": "Assiniboine",
    "Southboine": "Assiniboine",
    "Woodhaven": "Assiniboine",
    "Vialoux": "Assiniboine",
    "Birchwood": "Assiniboine",
    "Eric Coy": "Assiniboine",

    # East Kildonan area
    "East Elmwood": "East Kildonan",
    "Glenelm": "East Kildonan",
    "Rossmere-a": "East Kildonan",
    "Rossmere-b": "East Kildonan",
    "Eaglemere": "East Kildonan",
    "Valley Gardens": "East Kildonan",
    "River East": "East Kildonan",
    "Kildonan Drive": "East Kildonan",
    "Peguis": "East Kildonan",
    "Munroe East": "East Kildonan",
    "Munroe West": "East Kildonan",
    "Kildare-redonda": "East Kildonan",

    # West Kildonan area
    "West Kildonan Industrial": "West Kildonan",
    "Garden City": "West Kildonan",
    "Jefferson": "West Kildonan",
    "Riverbend": "West Kildonan",
    "Leila North": "West Kildonan",
    "Mandalay West": "West Kildonan",
    "Inkster Gardens": "West Kildonan",
    "Amber Trails": "West Kildonan",
    "Seven Oaks": "West Kildonan",

    # Fort Garry area
    "Fort Richmond": "Fort Garry",
    "Whyte Ridge": "Fort Garry",
    "Waverley West": "Fort Garry",
    "Fairfield Park": "Fort Garry",
    "Linden Woods": "Fort Garry",
    "University": "Fort Garry",
    "Chevrier": "Fort Garry",
    "Richmond West": "Fort Garry",
    "Montcalm": "Fort Garry",
    "Parc La Salle": "Fort Garry",
    "Bridgewater Trails": "Fort Garry",

    # St. James area
    "Silver Heights": "St. James",
    "Deer Lodge": "St. James",
    "Sturgeon Creek": "St. James",
    "Assiniboia Downs": "St. James",
    "Bruce Park": "St. James",
    "Crestview": "St. James",
    "Heritage Park": "St. James",
    "Westwood": "St. James",
    "Woodhaven": "St. James",

    # Downtown/Exchange area
    "Portage & Main": "Centennial",
    "South Point Douglas": "Centennial",
    "Exchange District": "Centennial",
    "The Forks": "Centennial",
    "Central Park": "Centennial",
    "Broadway-Assiniboine": "Centennial",
    "China Town": "Centennial",
    "Logan-c.p.r.": "Centennial",
    "Colony": "Centennial",
    "West Broadway": "Centennial",

    # St. Boniface area
    "Central St. Boniface": "St. Boniface",
    "South St. Boniface": "St. Boniface",
    "Norwood East": "St. Boniface",
    "Norwood West": "St. Boniface",
    "North St. Boniface": "St. Boniface",
    "Mission Gardens": "St. Boniface",
    "Dufresne": "St. Boniface",

    # Transcona area
    "Canterbury Park": "Transcona",
    "Mission Gardens": "Transcona",
    "Transcona South": "Transcona",
    "Transcona North": "Transcona",
    "Transcona Yards": "Transcona",
    "Kildonan Crossing": "Transcona",

    # Miscellaneous Submarkets (Assign where necessary)
    "Brooklands": "St. James",
    "Inkster Industrial Park": "West Kildonan",
    "Linden Ridge": "Fort Garry",
    "Royalwood": "St. Vital",
    "Kil-cona Park": "East Kildonan",
    "South Point Douglas": "Downtown",
    "Tuxedo": "Fort Garry",
    "Bridgewater Forest": "Fort Garry",
    "Grant Park": "Fort Rouge",

    # Unknown neighborhoods (label as 'Unknown' for manual review)
    "Margaret Park": "West Kildonan",
    "Templeton-sinclair": "West Kildonan",
    "Valhalla": "East Kildonan",
    "Elm Park": "St. Vital",
    "Maple Grove Park": "St. Vital",
    "Ridgewood South": "Assiniboine Park",
    "Sargent Park": "Midland",
    "Bruce Park": "Assiniboine Park",
    "Tyndall Park": "Lord Selkirk",
    "Grassie": "East Kildonan",
    "Parker": "Fort Rouge",
    "Wolseley":"Midland",
    "Burrows-keewatin": "Lord Selkirk",
    "Mcleod Industrial": "East Kildonan",
    "Brockville": "Assiniboine Park",
    "South River Heights":"Fort Rouge",
    "Earl Grey":"Fort Rouge",
    "Maybank":"Fort Garry",
    "Rivergrove": "West Kildonan",
    "Weston":"Centennial",
    "Daniel Mcintyre":"Midland",
    "Old Tuxedo":"Assiniboine Park",
    "Cloutier Drive":"Fort Garry",
    "Point Road":"Fort Garry",
    
    "Springfield North":"East Kildoman",
    "Holden": "St Boniface",
    "Mathers": "Assiniboine Park",
    "Lord Selkirk Park": "Lord Selkirk",
    "Centennial": "Centennial",
    "Glendale": "St James",
    "Buchanan": "St James",
    "Elmhurst": "Assiniboine Park",
    "Talbot-grey": "East Kildoman",
    "South Tuxedo": "Assiniboine Park",
    "Regent": "Transcona",
    "Dugald": "St Boniface",
    "Tyne-tees": "East Kildonan",
    "St. James Industrial": "St James",
    "Broadway-assiniboine": "Centennial",
    "Minto": "Midland",
    "Griffin": "Transcona",
    "Rockwood": "Fort Rouge",
    "Spence": "Centennial",
    "Stock Yards": "St Boniface",
    "Niakwa Place": "St Boniface",
    "Lavalee": "St Vital",
    "Legislature": "Centennial",
    "River-osborne": "Fort Rouge",
    "Burrows Central": "Lord Selkirk",
    "Maginot": "St Boniface",
    "Central River Heights": "Assiniboine Park",
    "J. B. Mitchell": "Assiniboine Park",
    "St. Vital Perimeter South": "St Vital",
    "Polo Park": "Midland",
    "West Wolseley": "Midland",
    "Edgeland": "Assiniboine Park",
    "River West Park": "Assiniboine Park",
    "Saskatchewan North": "St James",
    "St. George": "St Vital",
    "St. Norbert": "Fort Garry",
    "Springfield South": "East Kildonan",
    "North Transcona Yards": "East Kildonan",
    "West Fort Garry Industrial": "Fort Garry",
    "North Point Douglas": "Lord Selkirk",
    "St. John's Park": "Lord Selkirk",
    "Kirkfield": "St James",
    "Buffalo": "Fort Garry",
    "Pacific Industrial": "Centennial",
    "Alpine Place": "St Vital",
    "Kildonan Park": "West Kildonan",
    "Crescent Park": "Fort Garry",
    "Kingston Crescent": "St Vital",
    "Dufferin Industrial": "Lord Selkirk",
    "Luxton": "Lord Selkirk",
    "Rosser-old Kildonan": "West Kildonan",
    "Leila-mcphillips Triangle": "West Kildonan",
    "St. Vital Centre": "St Vital",
    "St. John's": "Lord Selkirk",
    "Jameswood": "St James",
    "Glenwood": "St Vital",
    "Oak Point Highway": "Lord Selkirk or Assiniboine Park",
    "Mynarski": "Lord Selkirk",
    "North Inkster Industrial": "Lord Selkirk",
    "Inkster-faraday": "Lord Selkirk",
    "King Edward": "St James",
    "Airport": "St James",
    "The Maples": "West Kildonan",
    "Murray Industrial Park": "St James",
    "William Whyte": "Lord Selkirk",
    "Dufferin": "Lord Selkirk",
    "Booth": "St James",
    "Agassiz": "Fort Garry",
    "Wilkes South": "Assiniboine Park",
    "Normand Park": "St Vital",
    "Turnbull Drive": "Fort Garry",
    "South Portage": "Centennial",
    "Trappistes": "Fort Garry",
    "Tuxedo Industrial": "Assiniboine Park",
    "St. Boniface Industrial Park": "St Boniface",
    "North River Heights": "Assiniboine Park",
    "Vista": "St Vital",
    "Waverley Heights": "Fort Garry",
    "Mcmillan": "Fort Rouge",
    "Robertson": "Lord Selkirk",
    "The Mint": "St Boniface",
    "St. Matthews": "Midland",
    "Archwood": "St Boniface",
    "Kern Park": "Transcona",
    "Melrose": "Transcona",
    "Victoria West": "Transcona",
    "Radisson": "Transcona",
    "Symington Yards": "St Boniface",
    "West Perimeter South": "Assiniboine Park",
    "Civic Centre": "Centennial",
    "Tissot": "St Boniface",
    "Meadows": "East Kildonan",
    "Omand's Creek Industrial": "St James",
    "Mission Industrial": "St Boniface",
    "Shaughnessy Park": "Lord Selkirk",
    "Weston Shops": "Lord Selkirk",
    "Roblin Park": "Assiniboine Park",
    "Kensington": "St James",
    "Chalmers": "East Kildonan",
    "La Barriere": "Fort Garry",
    "Sir John Franklin": "Assiniboine Park",
    "Perrault": "Fort Garry",
    "Richmond Lakes": "Fort Garry",
    "Southland Park": "St Boniface",
    "Varsity View": "Assiniboine Park",
    "West Alexander": "Centennial",
    "Portage-ellice": "Centennial",
    "Betsworth": "Assiniboine Park",
    "Marlton": "Assiniboine Park",
    "Westdale": "Assiniboine Park",
    "Beaumont": "Fort Garry",
    "Pembina Strip": "Fort Garry",
    "Ridgedale": "Assiniboine Park"
    
    
}


# Geocode the address
def geocode_address(address):
    """
    Convert an address into latitude and longitude using Nominatim.
    """
    geolocator = Nominatim(user_agent="cmhc-zone-finder")
    location = geolocator.geocode(address)
    if location:
        print("The coordinates of this address is", location)
        return Point(location.longitude, location.latitude)  # Longitude, Latitude for Shapely
        
    return None

# Find the CMHC zone
def find_cmhc_zone(address):
    """
    Find the neighborhood and CMHC zone for the given address.
    """
    point = geocode_address(address)
    if point is None:
        return {"error": "Address could not be geocoded."}

    # Check which neighborhood contains the point
    for _, row in neighborhoods.iterrows():
        if row["geometry"].contains(point):
            neighborhood_name = row["Name"]
            cmhc_zone = neighborhood_to_cmhc.get(neighborhood_name, "Unknown")
            return {"neighborhood": neighborhood_name, "cmhc_zone": cmhc_zone}
            

    return {"error": "No neighborhood found for this address."}

# Flask routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_zone", methods=["POST"])
def get_zone():
    address = request.form.get("address")
    if not address:
        return jsonify({"error": "Address is required."})

    point = geocode_address(address)
    if not point:
        return jsonify({"error": "Address could not be geocoded."})

    found_neighborhood = None
    for _, row in neighborhoods.iterrows():
        if row["geometry"].contains(point):
            found_neighborhood = row
            break

    if found_neighborhood is None:
        return jsonify({"error": "No neighborhood found for this address."})

    neighborhood_name = found_neighborhood["Name"]
    cmhc_zone = neighborhood_to_cmhc.get(neighborhood_name, "Unknown")

    m = folium.Map(location=[point.y, point.x], zoom_start=14)

    folium.Marker(
        [point.y, point.x],
        popup="Input Location",
        icon=folium.Icon(color="red")
    ).add_to(m)

    folium.GeoJson(
        found_neighborhood["geometry"].__geo_interface__,
        name=f"{neighborhood_name} Area",
        tooltip=neighborhood_name
    ).add_to(m)

    map_html = m._repr_html_()

    return jsonify({
        "neighborhood": neighborhood_name,
        "cmhc_zone": cmhc_zone,
        "map": map_html
    })


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
