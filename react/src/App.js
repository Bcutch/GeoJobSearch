import DisplayJobs from "./components/DisplayJobs";
import Filtering from "./components/Filtering";
import NavigationBar from "./components/NavigationBar";
import Search from "./components/Search";
import React, { useState, useEffect } from "react";

function App() {
  const [jobs, setJobs] = useState([]);

  return (
    <div>
      <NavigationBar />
      <main>
        <Search />
        <Filtering setJobs={setJobs}/>
        <DisplayJobs /*jobs={jobs} setJobs={setJobs}*//>
      </main>
    </div>
  );
}

export default App;
