export default function Disclaimer() {
  return (
    <div className="min-h-screen bg-[#0f172a] text-white px-6 py-16">
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-4xl font-bold mb-6">Disclaimer</h1>

        <p>
          CivicResolve provides analytical insights and system monitoring tools.
        </p>

        <h2 className="text-2xl font-semibold mt-6">Accuracy of Information</h2>
        <p>
          While we strive for accuracy, we do not guarantee complete reliability of predictions.
        </p>

        <h2 className="text-2xl font-semibold mt-6">External Links</h2>
        <p>
          The platform may contain links to third-party resources. We are not responsible for their content.
        </p>

        <p className="text-gray-400 mt-8">
          Last updated: 2026
        </p>
      </div>
    </div>
  );
}
