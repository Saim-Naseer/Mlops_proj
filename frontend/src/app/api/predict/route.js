export async function POST(req) {
  const body = await req.json();

  // Call FastAPI backend
  const backendRes = await fetch("http://backend:8000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const data = await backendRes.json();

  return new Response(JSON.stringify({ prediction: data.chance_of_admission }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}