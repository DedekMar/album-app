/* eslint-disable react/prop-types */
export default function AlbumSearch({
  onTextChange,
  onSearch,
  albumSearchText,
}) {
  return (
    <>
      <input
        type="text"
        placeholder="Search album by name"
        value={albumSearchText}
        onChange={(e) => onTextChange(e)}
      ></input>
      <button onClick={() => onSearch()}>Search</button>
    </>
  );
}
