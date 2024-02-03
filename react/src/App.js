import DisplayJobs from "./components/DisplayJobs";
import Filtering from "./components/Filtering";
import NavigationBar from "./components/NavigationBar";

function App() {
  return (
    <div>
      <NavigationBar />
      <main>
        <Filtering />
        <DisplayJobs />
      </main>
    </div>
  );
}

export default App;
