import React from 'react';

function SearchTextList({ searchTexts, onSearchTextClick }) {
  return (
    <div>
      <h2>Prodotti Cercati</h2>
      <ul>
        {searchTexts.map((searchText, index) => (
          <li key={index} onClick={() => onSearchTextClick(searchText)}>
            <button>{searchText}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SearchTextList;
