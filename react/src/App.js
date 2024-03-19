import React from "react";
import Filtering from "./components/Filtering";
import NavigationBar from "./components/NavigationBar";
import Search from "./components/Search";
import Map from "./components/Map"
import DisplayJobs from "./components/DisplayJobs";
import { useState } from "react";

function App() {

  const [jobs, setJobs] = useState([]);

  return (
    <div>
      <NavigationBar />
      <Map />
      <main>
        <Search />
        <Filtering setJobs = {setJobs}/>
        <DisplayJobs jobs = {jobs} setJobs = {setJobs}/>
      </main>
    </div>
  );
}

export default App;
