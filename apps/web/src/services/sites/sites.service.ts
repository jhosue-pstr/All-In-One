import api from "../api";
import type { Site, SiteCreate } from "../../types";

export const sitesService = {
  getAll: async (): Promise<Site[]> => {
    const response = await api.get<Site[]>("/sites");
    return response.data;
  },

  create: async (data: SiteCreate): Promise<Site> => {
    const response = await api.post<Site>("/sites", data);
    return response.data;
  },

  getById: async (id: number): Promise<Site> => {
    const response = await api.get<Site>(`/sites/${id}`);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/sites/${id}`);
  },
};
