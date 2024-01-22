import React, { useState, useEffect } from "react";
import SearchTextList from "./components/SearchTextList";
import PriceHistoryTable from "./components/PriceHistoryTable";
import axios from "axios";
import TrackedProductList from "./components/TrackedProductList";

// const URL = "http://172.17.0.3:5000";
const URL = "http://localhost:5000";

const SEARCH_URLS = {
  SOCCAVO: "https://www.farmaciasoccavo.it",
  // LORETO: "https://farmacialoreto.it",
  EFARMA: "https://www.efarma.com"
}

function App() {
  const [showPriceHistory, setShowPriceHistory] = useState(false);
  const [priceHistory, setPriceHistory] = useState([]);
  const [searchTexts, setSearchTexts] = useState([]);
  const [newSearchText, setNewSearchText] = useState("");

  useEffect(() => {
    fetchUniqueSearchTexts();
  }, []);

  const fetchUniqueSearchTexts = async () => {
    try {
      const response = (await axios.get(`${URL}/unique_search_texts`))
      const data = response.data;
      setSearchTexts(data);
    } catch (error) {
      console.error("Error fetching unique search texts:", error);
    }
  };
  // on selected product from previous search, calls GET /results?search_text=....
  const handleSearchTextClick = async (searchText) => {
    try {
      const response = await axios.get(
        `${URL}/results?search_text=${searchText}`
      );

      const data = response.data;
      setPriceHistory(data);
      setShowPriceHistory(true);
    } catch (error) {
      console.error("Error fetching price history:", error);
    }
  };

  const handlePriceHistoryClose = () => {
    setShowPriceHistory(false);
    setPriceHistory([]);
  };

  const handleNewSearchTextChange = (event) => {
    setNewSearchText(event.target.value);
  };
  // LAUNCHES THE SCRAPER -> POST to /start-scraper
  const handleNewSearchTextSubmit = async (event) => {
    event.preventDefault();

    try {
      for (const search_url in SEARCH_URLS) {
        console.log("URL is:", SEARCH_URLS[search_url])
        console.log("Starting scraper for", search_url)
        await axios.post(`${URL}/start-scraper`, {
          search_text: newSearchText,
          url: SEARCH_URLS[search_url],
        });
      }

      alert("Scraper started successfully");
      setSearchTexts([...searchTexts, newSearchText]);
      setNewSearchText("");
    } catch (error) {
      alert("Error starting scraper:", error);
    }
  };

  return (
    <div className="main">
      <div style={{ textAlign: "center" }}>
        <h1>Cerca Farmaco</h1>
        <form onSubmit={handleNewSearchTextSubmit}>
          <label>Inserisci il farmaco da cercare:</label>
          <input
            type="text"
            value={newSearchText}
            onChange={handleNewSearchTextChange}
          />
          <button type="submit">Cerca</button>
        </form>
      </div>
      <SearchTextList
        searchTexts={searchTexts}
        onSearchTextClick={handleSearchTextClick}
      />
      {/* <TrackedProductList /> */}
      {showPriceHistory && (
        <PriceHistoryTable
          priceHistory={priceHistory}
          onClose={handlePriceHistoryClose}
        />
      )}
    </div>
  );
}

export default App;
