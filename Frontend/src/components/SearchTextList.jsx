import React from 'react';

function SearchTextList({ searchTexts, onSearchTextClick }) {
  return (
    <div style={{ width: "50%", margin: "auto" }}>
      <h2 style={{ textAlign: "center" }}>Farmaci Cercati</h2>
      <ul style={{ columns: 2 }}>
        {searchTexts.map((searchText, index) => (
          <li key={index}>
            <button onClick={() => onSearchTextClick(searchText)}>{searchText}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchTextList;
