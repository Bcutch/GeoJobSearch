import DisplayJobs from "./components/DisplayJobs";
import Filtering from "./components/Filtering";
import NavigationBar from "./components/NavigationBar";
import Search from "./components/Search";

function App() {
  return (
    <div>
      <NavigationBar />
      <main>
        <Search />
        <Filtering />
        <DisplayJobs />
      </main>
    </div>
  );
}

export default App;
