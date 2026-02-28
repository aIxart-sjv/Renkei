import client from "./client";

export const getRecommendations = async (userId) => {
  const response = await client.get(
    `/recommendations/full/${userId}`
  );
  return response.data;
};