import { useState } from "react";
import { ChevronDown } from "lucide-react";

type Faq = {
  question: string;
  answer: string;
};

const faqs: Faq[] = [
  {
    question: "What is meant by enrolment saturation?",
    answer:
      "Enrolment saturation refers to regions where Aadhaar coverage has reached near-universal levels and new enrolments show minimal growth.",
  },
  {
    question: "Why are demographic updates higher in urban areas?",
    answer:
      "Urban regions experience higher address and mobile number changes due to migration, employment mobility, and housing transitions.",
  },
  {
    question: "Which age group initiates the most updates?",
    answer:
      "Residents aged 18 and above initiate the highest number of demographic updates, primarily for address and mobile number changes.",
  },
  {
    question: "How is biometric update churn measured?",
    answer:
      "Biometric churn is measured using repeat capture frequency due to ageing, occupation-related wear, or biometric quality degradation.",
  },
];

export default function FaqSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <div className="faq-section">
      <h3 className="section-title">Frequently Asked Questions</h3>

      {faqs.map((faq, index) => (
        <div key={index} className="faq-item">
          <button
            className="faq-question"
            onClick={() =>
              setOpenIndex(openIndex === index ? null : index)
            }
          >
            <span>{faq.question}</span>
            <ChevronDown
              size={16}
              className={openIndex === index ? "rotate" : ""}
            />
          </button>

          {openIndex === index && (
            <div className="faq-answer">{faq.answer}</div>
          )}
        </div>
      ))}
    </div>
  );
}
