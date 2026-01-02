export default function Facts() {

  const bibliography: { id: number; title: string; url: string }[] = [
    {
      id: 1,
      title: "HubSpot/SurveyMonkey Report",
      url: "https://offers.hubspot.com/ai-report-surveymonkey"
    },
    {
      id: 2,
      title: "CivicScience Survey",
      url: "https://civicscience.com/customer-service-chatbots-earn-mixed-reviews-as-people-still-prefer-human-conversations/"
    },
    {
      id: 3,
      title: "Washington State/Temple University Study",
      url: "https://news.wsu.edu/press-release/2024/07/30/using-the-term-artificial-intelligence-in-product-descriptions-reduces-purchase-intentions/"
    },
  ];

  return (
    <div>
      <h1>The Ugly Truth about Consumer Preferences and Chat Inter</h1>
      <ul class="facts-list">
        <li>53% of consumers dislike or hate AI in customer service, reflecting failure to meet expectations for empathy and nuance. <a href="#ref-1"><sup>[1]</sup></a></li>
        <li>45% find customer service chatbots unfavorable, up from 43% in 2022, with only 19% viewing them as favorable. <a href="#ref-2"><sup>[2]</sup></a></li>
        <li>82% prefer human support over AI, even with identical wait times/outcomes, prioritizing empathy. <a href="#ref-1"><sup>[1]</sup></a></li>
        <li>Only 17% prefer chatbots for post-purchase support, versus 43% for phone/human interactions. <a href="#ref-2"><sup>[2]</sup></a></li>
        <li>AI decreases emotional trust, reducing purchase intentions by 24%, especially for high-risk buys. <a href="#ref-3"><sup>[3]</sup></a></li>
        <li>Only 25% like or love AI in customer service, positioning it as a frustration-inducing barrier. <a href="#ref-1"><sup>[1]</sup></a></li>
        <li>Only 7% of ages 55+ find chatbots favorable, compared to 37% for Gen Z, highlighting generational gaps. <a href="#ref-2"><sup>[2]</sup></a></li>
      </ul>
    </div>
  )
}
