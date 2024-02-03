import DisplayJobs from "./components/DisplayJobs";
import NavigationBar from "./components/NavigationBar";

function App() {
  return (
    <div>
      <NavigationBar />
      <main>
        <DisplayJobs />
      </main>
    </div>
  );
}

export default App;
