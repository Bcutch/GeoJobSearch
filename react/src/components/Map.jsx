import React from "react";
import { MapContainer, TileLayer } from 'react-leaflet'

export default function Map() {
    return (
        <MapContainer center={[43.5448,-80.2482]} zoom={14} style={{ height: '500px', width: '100%' }}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}"
                id="mapbox/dark-v10"
                tileSize={512}
                zoomOffset={-1}
                accessToken="pk.eyJ1IjoibmVkYXNraWJpbGRpcyIsImEiOiJjbHRqMmMyNXQwbGwzMm1wNWlkbHh5ZXBrIn0.Bb5m8mQ0V7sfrxTrhWYEbA"
            />
        </MapContainer>
    )
}
