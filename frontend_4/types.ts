
export type Role = 'Admin' | 'Worker' | 'Camera';

export interface UserSession {
  username: string;
  role: Role;
  displayName: string;
}

export interface LocationData {
  lat: number;
  lng: number;
  address: string;
}

export interface IncidentImages {
  original: string;
  resolved?: string;
}

export interface IncidentReport {
  id: number;
  type: string;
  status: 'pending' | 'completed' | 'verified';
  location: LocationData;
  images: IncidentImages;
  assigned_to?: string;
  created_at?: string;
}

export interface AIPrediction {
  class: string;
  confidence: number;
}

export interface AIResponse {
  count: number;
  predictions: AIPrediction[];
}
