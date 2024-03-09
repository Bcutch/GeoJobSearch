import DisplayJobs from "./components/DisplayJobs";
import Filtering from "./components/Filtering";
import NavigationBar from "./components/NavigationBar";
import Search from "./components/Search";
import Map from "./components/Map"

function App() {
  return (
    <div>
      <NavigationBar />
      <Map />
      <main>
        <Search />
        <Filtering />
        <DisplayJobs />
      </main>
    </div>
  );
}

export default App;
