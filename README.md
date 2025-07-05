# 🚖 Cab Fare Comparator

This project automates the process of checking and comparing real-time taxi fare estimates from **Rapido** and **GoByTaxi** websites using **Selenium WebDriver** in Python. It helps users decide the most cost-effective cab option for a given pickup and drop location.

## 📌 Features

- ✅ Scrapes real-time fares from Rapido and GoByTaxi.
- 🔄 Compares and highlights the cheaper option.
- 💾 Saves all results in a combined `compared.json` file.
- 🧪 Modular structure with separate scripts for each platform (`rapido.py`, `goby.py`).
- ⚡ Bypasses most ads or waits for manual closure on ad-blocked pages.

---

## 📁 Project Structure

cab-fare-comparator/
│
├── rapido.py # Scrapes fare data from Rapido
├── goby.py # Scrapes fare data from GoByTaxi
├── compare.py # Executes both scripts, compares results, saves final output
├── rapido_fare.json # Output from rapido.py
├── gobytaxi_fare.json# Output from goby.py
├── compared.json # Final comparison result
├── requirements.txt # Python package dependencies
└── README.md # This file


---

## ⚙️ Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/cab-fare-comparator.git
   cd cab-fare-comparator

📝 Sample Output (compared.json)
json
Copy
Edit
{
  "pickup": "Koramangala, Bengaluru",
  "drop": "Indiranagar, Bengaluru",
  "rapido_cab_premium": "₹197",
  "gobytaxi": "₹373",
  "best_option": "Rapido (Cab Premium)",
  "book_url": "https://m.rapido.bike/unup-home/seo/Koramangala%2C%20Bengaluru/Indiranagar%2C%20Bengaluru?version=v3",
  "timestamp": "2025-07-04 21:58:07"
}
