
const TrackComponent = ({ track }) => {
    // Destructuring the track object
    const { track_title, grade, for_distrokid, uploads } = track;
  
    return (
      <div>
        <h2>Track Details</h2>
        <p>Track Title: {track_title}</p>
        <p>Grade: {grade}</p>
        <p>For DistroKid: {for_distrokid.toString()}</p> {/* Converting boolean to string for display */}
        <h3>Uploads</h3>
        {/* Rendering upload details for each platform */}
        <ul>
          {Object.keys(uploads).map((platform) => (
            <li key={platform}>
              {platform}:
              <ul>
                <li>Upload Attempts: {uploads[platform].upload_attempts.length}</li>
              </ul>
            </li>
          ))}
        </ul>
      </div>
    );
  };
  
  export default TrackComponent;