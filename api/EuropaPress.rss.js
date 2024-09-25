export default async function handler(req, res) {
  const rssFeedUrl = 'https://lovetv.synology.me:4433/EuropaPress.rss';  // Replace with the actual Europa Press RSS feed URL

  try {
    // Fetch the content from the Europa Press RSS feed URL
    const response = await fetch(rssFeedUrl);

    // If the response is not OK, return an error
    if (!response.ok) {
      return res.status(response.status).json({ error: 'Failed to fetch RSS feed' });
    }

    // Get the content type and RSS feed data
    const contentType = response.headers.get('content-type');
    const rssContent = await response.text();

    // Set the content type header and return the fetched RSS feed
    res.setHeader('Content-Type', contentType);
    res.status(200).send(rssContent);
  } catch (error) {
    // Handle errors
    console.error('Error fetching RSS feed:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}

