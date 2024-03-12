import React, { useState, useEffect } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";

const Filtering = () => {
  // State for the titles of the dropdown buttons
  const [jobType, setJobType] = useState("Job Type");
  const [remote, setRemote] = useState("Remoteness");
  const [salary, setSalary] = useState("Salary");
  const [distance, setDistance] = useState("Distance");

  useEffect(() => {

    var cat = Object.assign({}, {jobType}, {remote}, {salary}, {distance});
    //var catstr = "'"+JSON.stringify( cat )+"'";
    //console.log(catstr);

    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify( cat )
    };

    fetch("http://localhost:8080/jobs", requestOptions)
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error filtering jobs:", error));
  }, [jobType, remote, salary, distance]);

  // Handler functions to update state based on the selected item's eventKey
  const handleJobTypeSelect = (eventKey) => {
    setJobType(eventKey);
  };

  const handleRemoteSelect = (eventKey) => {
    setRemote(eventKey);
  };

  const handleSalarySelect = (eventKey) => {
    setSalary(eventKey);
  };
  
  const handleDistanceSelect = (eventKey) => {
    setDistance(eventKey);
  };

  return (
    <div className="flex gap-2 justify-center p-4">
      <DropdownButton title={jobType} onSelect={handleJobTypeSelect}>
        <Dropdown.Item eventKey="Full-time">Full-time</Dropdown.Item>
        <Dropdown.Item eventKey="Part-time">Part-time</Dropdown.Item>
        <Dropdown.Item eventKey="Internship">Internship</Dropdown.Item>
      </DropdownButton>
      <DropdownButton title={remote} onSelect={handleRemoteSelect}>
        <Dropdown.Item eventKey="Remote">Remote</Dropdown.Item>
        <Dropdown.Item eventKey="Hybrid">Hybrid</Dropdown.Item>
        <Dropdown.Item eventKey="On-Site">On-site</Dropdown.Item>
      </DropdownButton>
      <DropdownButton title={salary} onSelect={handleSalarySelect}>
        <Dropdown.Item eventKey="$0-$50k">$0-$50k</Dropdown.Item>
        <Dropdown.Item eventKey="$50k-$100k">$50k-$100k</Dropdown.Item>
        <Dropdown.Item eventKey="$100k-$150k">$100k-$150k</Dropdown.Item>
        <Dropdown.Item eventKey="$150k-$200k">$150k-$200k</Dropdown.Item>
        <Dropdown.Item eventKey="$200k+">$200k+</Dropdown.Item>
      </DropdownButton>
      <DropdownButton title={distance} onSelect={handleDistanceSelect}>
        <Dropdown.Item eventKey=">20km">less than 20km</Dropdown.Item>
        <Dropdown.Item eventKey=">50km">less than 50km</Dropdown.Item>
        <Dropdown.Item eventKey=">100km">less than 100km</Dropdown.Item>
        <Dropdown.Item eventKey=">150km">less than 150km</Dropdown.Item>
      </DropdownButton>
    </div>
  );
};

export default Filtering;
