export async function getAIMessage(message) {
  const res = await fetch("http://localhost:5000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ message })
  });


  if (!res.ok) {
    throw new Error("Chat request failed");
  }

  const data = await res.json();
  console.log(data.content);

  const html = data.content.map(block => {
    if (block.type === "text") {
      return block.value;
    }

    if (block.type === "image") {
      return `<img src="${block.src}" style="max-width:100%; margin:8px 0;" />`;
    }

    if (block.type === "youtube") {
      return `
        <iframe
          width="100%"
          height="315"
          src="https://www.youtube.com/embed/${block.videoId}"
          frameborder="0"
          allowfullscreen
        ></iframe>
      `;
    }

    return "";
  }).join("<br/>");

  return {
    role: "assistant",
    content: html
  };

}
