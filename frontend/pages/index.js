import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [taskId, setTaskId] = useState("");
  const [status, setStatus] = useState(null);

  const enqueue = async () => {
    const res = await axios.post("http://localhost:8000/enqueue");
    setTaskId(res.data.task_id);
  };

  const checkStatus = async () => {
    if (!taskId) return;
    const res = await axios.get(`http://localhost:8000/tasks/${taskId}`);
    setStatus(res.data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Dynamic Question Bank</h1>
      <button onClick={enqueue}>Enqueue Dummy Transcription</button>
      {taskId && (
        <>
          <p>Task ID: {taskId}</p>
          <button onClick={checkStatus}>Check Status</button>
          <pre>{JSON.stringify(status, null, 2)}</pre>
        </>
      )}
    </div>
  );
}
