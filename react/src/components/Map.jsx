import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import React, { useState, useEffect } from "react";

export default function Map() {
    const [jobs, setJobs] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8080/jobs")
        .then((response) => response.json())
        .then((data) => setJobs(data))
        .catch((error) => console.error("Error fetching jobs:", error));
    }, []);



    return (
        <> 
            {/* Create A Map Container Component, This is the basis for our dynamic map */}
            <MapContainer center={[43.5448,-80.2482]} zoom={14} style={{ height: '500px', width: '100%' }}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}"
                    id="mapbox/dark-v10"
                    tileSize={512}
                    zoomOffset={-1}
                    accessToken="pk.eyJ1IjoibmVkYXNraWJpbGRpcyIsImEiOiJjbHRqMmMyNXQwbGwzMm1wNWlkbHh5ZXBrIn0.Bb5m8mQ0V7sfrxTrhWYEbA"
                />
                {/* For every job in the database, if the longitude and latitude is not null, create a marker component that display the job in the map container */}
                {jobs.map((job, index) => (
                    job.latitude !== null && job.longitude !== null ? (
                        <Marker key={index} position={[job.latitude, job.longitude]}>
                            <Popup>
                                {job.title} <br /> {job.location}
                            </Popup>
                        </Marker>
                    ) : null
                ))}
           </MapContainer> 
        </>

    );
}
