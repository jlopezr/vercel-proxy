export default async function handler(req, res) {
  const { url } = req.query;

  // Validate the URL
  if (!url) {
    return res.status(400).json({ error: 'URL is required' });
  }

  try {
    // Fetch the content from the provided URL
    const response = await fetch(url);

    // If the response is not OK, return an error
    if (!response.ok) {
      return res.status(response.status).json({ error: 'Failed to fetch content' });
    }

    // Get the content type and return the content
    const contentType = response.headers.get('content-type');
    const content = await response.text();

    // Set the content type header and return the fetched content
    res.setHeader('Content-Type', contentType);
    res.status(200).send(content);
  } catch (error) {
    // Handle errors
    console.error('Error fetching content:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}

