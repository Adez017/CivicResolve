import Navbar from "@/components/Navbar";

export default function Disclaimer() {
  return (
    <div className="min-h-screen bg-[#0f172a] text-white px-6 py-20">
      <div className="max-w-4xl mx-auto">

        {/* Page Heading */}
        <h1 className="text-4xl md:text-5xl font-bold text-center mb-10 tracking-tight">
          Disclaimer
        </h1>

        {/* Intro */}
        <p className="text-gray-300 leading-relaxed text-lg mb-6">
          The information provided on CivicResolve is intended for general
          informational and analytical purposes only. While we strive to ensure
          accuracy and reliability, we make no guarantees regarding the completeness,
          timeliness, or accuracy of the information displayed on this platform.
        </p>

        {/* Section 1 */}
        <section className="mt-10">
          <h2 className="text-2xl font-semibold border-l-4 border-blue-500 pl-4 mb-4">
            1. Accuracy of Information
          </h2>
          <p className="text-gray-300 leading-relaxed">
            CivicResolve provides analytical insights and system monitoring tools
            based on available data. Although we aim to present accurate results,
            predictions and reports may vary due to data limitations, system updates,
            or external factors beyond our control.
          </p>
        </section>

        {/* Section 2 */}
        <section className="mt-10">
          <h2 className="text-2xl font-semibold border-l-4 border-blue-500 pl-4 mb-4">
            2. No Professional Advice
          </h2>
          <p className="text-gray-300 leading-relaxed">
            The content on this platform does not constitute legal, governmental,
            or professional advice. Users are encouraged to consult qualified
            professionals before making decisions based on information obtained
            from this website.
          </p>
        </section>

        {/* Section 3 */}
        <section className="mt-10">
          <h2 className="text-2xl font-semibold border-l-4 border-blue-500 pl-4 mb-4">
            3. External Links
          </h2>
          <p className="text-gray-300 leading-relaxed">
            CivicResolve may include links to third-party websites or services.
            We do not control or endorse the content, policies, or practices of
            external platforms and are not responsible for any information or
            services provided by them.
          </p>
        </section>

        {/* Section 4 */}
        <section className="mt-10">
          <h2 className="text-2xl font-semibold border-l-4 border-blue-500 pl-4 mb-4">
            4. Limitation of Liability
          </h2>
          <p className="text-gray-300 leading-relaxed">
            Under no circumstances shall CivicResolve or its team be held liable
            for any direct, indirect, incidental, or consequential damages arising
            from the use of this platform.
          </p>
        </section>

        {/* Footer Note */}
        <div className="mt-16 text-sm text-gray-400 text-center border-t border-gray-700 pt-6">
          Last updated: 2026
        </div>

      </div>
    </div>
  );
}