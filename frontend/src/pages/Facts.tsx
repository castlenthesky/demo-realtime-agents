import { createSignal, For, onCleanup, onMount } from 'solid-js';

export default function Facts() {
  const [activeRef, setActiveRef] = createSignal<string | null>(null);

  const updateActiveRef = (refId?: string) => {
    const hash = refId || window.location.hash;
    if (hash) {
      const id = hash.startsWith('#') ? hash.substring(1) : hash;
      if (id.startsWith('ref-')) {
        setActiveRef(id);
        
        // Smooth scroll to the reference
        setTimeout(() => {
          const element = document.getElementById(id);
          if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }, 100);
      } else {
        setActiveRef(null);
      }
    } else {
      setActiveRef(null);
    }
  };

  const handleRefClick = (refId: string) => {
    // Update immediately for instant feedback
    setActiveRef(refId);
    // Also update URL hash (browser will handle navigation)
    window.location.hash = `#${refId}`;
    // Scroll to the reference
    setTimeout(() => {
      const element = document.getElementById(refId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);
  };

  onMount(() => {
    const handleHashChange = () => {
      updateActiveRef();
    };

    // Check on mount
    updateActiveRef();

    // Listen for hash changes
    window.addEventListener('hashchange', handleHashChange);

    onCleanup(() => {
      window.removeEventListener('hashchange', handleHashChange);
    });
  });

  const bibliography = [
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
    {
      id: 4,
      title: "a16z State of Consumer AI Report",
      url: "https://a16z.com/state-of-consumer-ai-2025-product-hits-misses-and-whats-next/"
    }
  ];

  return (
    <div>
      <h1>The Ugly Truth about Consumer Preference</h1>
      <ul class="facts-list">
        <li>53% of consumers dislike or hate AI in customer service, reflecting failure to meet expectations for empathy and nuance. <a href="#ref-1" onClick={() => handleRefClick('ref-1')}><sup>[1]</sup></a></li>
        <li>45% find customer service chatbots unfavorable, up from 43% in 2022, with only 19% viewing them as favorable. <a href="#ref-2" onClick={() => handleRefClick('ref-2')}><sup>[2]</sup></a></li>
        <li>82% prefer human support over AI, even with identical wait times/outcomes, prioritizing empathy. <a href="#ref-1" onClick={() => handleRefClick('ref-1')}><sup>[1]</sup></a></li>
        <li>Only 17% prefer chatbots for post-purchase support, versus 43% for phone/human interactions. <a href="#ref-2" onClick={() => handleRefClick('ref-2')}><sup>[2]</sup></a></li>
        <li>AI decreases emotional trust, reducing purchase intentions by 24%, especially for high-risk buys. <a href="#ref-3" onClick={() => handleRefClick('ref-3')}><sup>[3]</sup></a></li>
        <li>Only 25% like or love AI in customer service, positioning it as a frustration-inducing barrier. <a href="#ref-1" onClick={() => handleRefClick('ref-1')}><sup>[1]</sup></a></li>
        <li>Low retention for new AI interfaces, with sub-8% day-30 retention for some apps due to cluttered experiences. <a href="#ref-4" onClick={() => handleRefClick('ref-4')}><sup>[4]</sup></a></li>
        <li>Only 7% of ages 55+ find chatbots favorable, compared to 37% for Gen Z, highlighting generational gaps. <a href="#ref-2" onClick={() => handleRefClick('ref-2')}><sup>[2]</sup></a></li>
      </ul>
      <section class="bibliography">
        <h2>Bibliography</h2>
        <ol class="bibliography-list">
          <For each={bibliography}>
            {(ref) => (
              <li 
                id={`ref-${ref.id}`}
                class={activeRef() === `ref-${ref.id}` ? 'active' : ''}
              >
                <a href={ref.url} target="_blank" rel="noopener noreferrer">
                  {ref.title}
                </a>
              </li>
            )}
          </For>
        </ol>
      </section>
    </div>
  )
}
