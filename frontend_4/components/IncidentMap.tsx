import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { IncidentReport } from '../types';
import L from 'leaflet';

// Use CDN URLs for Leaflet assets to ensure compatibility in the browser ESM environment
const iconUrl = 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png';
const iconRetinaUrl = 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png';
const shadowUrl = 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
  iconUrl,
  iconRetinaUrl,
  shadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});

// Apply the fix to all markers
L.Marker.prototype.options.icon = DefaultIcon;

interface IncidentMapProps {
  incidents: IncidentReport[];
  center?: [number, number];
  zoom?: number;
}

const IncidentMap: React.FC<IncidentMapProps> = ({ 
  incidents, 
  center = [12.9716, 77.5946], 
  zoom = 13 
}) => {
  return (
    <div className="h-full w-full rounded-xl overflow-hidden shadow-inner border border-gray-200">
      <MapContainer center={center} zoom={zoom} scrollWheelZoom={false} className="h-full w-full">
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {incidents.map((incident) => (
          <Marker 
            key={incident.id} 
            position={[incident.location.lat, incident.location.lng]}
          >
            <Popup>
              <div className="text-sm">
                <p className="font-bold text-indigo-600 uppercase">{incident.type}</p>
                <p className="text-gray-600">{incident.location.address}</p>
                <p className={`mt-1 font-semibold ${incident.status === 'pending' ? 'text-amber-500' : incident.status === 'completed' ? 'text-blue-500' : 'text-emerald-500'}`}>
                  Status: {incident.status}
                </p>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default IncidentMap;