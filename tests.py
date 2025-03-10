import unittest
from earthquake_risk_logic import extract_state_from_place, analyse_state_risk, assess_location_risk
from data import CLIENT_LOCATIONS

class TestEarthquakeRiskAssessor(unittest.TestCase):
    
    def test_extract_state_from_place(self):
        """Test if we can correctly find state abbreviations from place names."""
        self.assertEqual(extract_state_from_place("10km N of Los Angeles, CA"), "CA")
        self.assertEqual(extract_state_from_place("5km S of Reno, Nevada"), "NV")
         # although we are excluding Hawaii from the results, this test makes sure we can correctly identify Hawaii to be able to exclude it 
        self.assertEqual(extract_state_from_place("20km E of Honolulu, HI"), "HI")
        self.assertIsNone(extract_state_from_place("Somewhere, ?"))

    def test_analyse_state_risk(self):
        """Test if state quake counts and magnitudes are calculated right, skipping Hawaii."""
        sample_data = {
            "features": [
                {"properties": {"place": "10km N of Los Angeles, CA", "mag": 2.5}},
                {"properties": {"place": "5km S of Reno, NV", "mag": 3.0}},
                {"properties": {"place": "20km E of Honolulu, HI", "mag": 4.0}}
            ]
        }
        counts, mags = analyse_state_risk(sample_data)
        self.assertEqual(counts["CA"], 1)  
        self.assertNotIn("HI", counts)    
        self.assertEqual(mags["NV"], 3.0)

    def test_assess_location_risk(self):
            """Test if location risk is calculated correctly for West Anchorage High School."""
            sample_data = {
                "features": [
                    {"properties": {"place": "Right at Anchorage High School, AK", "mag": 1.5}, 
                    "geometry": {"coordinates": [-149.8997, 61.2163]}},
                    {"properties": {"place": "Middle of Pacific Ocean", "mag": 3.0}, 
                    "geometry": {"coordinates": [-170.0, 20.0]}}
                ]
            }
            risks = assess_location_risk(sample_data, [CLIENT_LOCATIONS[0]], radius_km=10)
            anchorage_risk = risks["West Anchorage High School"]
            self.assertEqual(anchorage_risk["nearby_quakes"], 1)
            self.assertEqual(anchorage_risk["avg_magnitude"], 1.5)
            self.assertEqual(anchorage_risk["risk_score"], 1.5)

if __name__ == "__main__":
    unittest.main()