import { useState } from "react";
import SiteLogo from "./assets/icon.svg";
import EvlLogo from "./assets/envl.svg";
import "./App.css";
import { enrolmentTrendData, updateTrendData } from "./data.ts";
import AadhaarTrendChart from "./components/AadhaarTrendChart.tsx";
import {
  Users,
  Fingerprint,
  FileText,
  MapPin,
  TrendingUp,
  BarChart3,
  AlertTriangle,
  Baby,
  School,
  Building2,
  Home,
} from "lucide-react";

import KpiCard from "./components/KpiCard";
import UrbanRuralChurnPie from "./components/UrbanRuralChurnPie";
import FaqSection from "./components/FaqSection";
import AskQuestionForm from "./components/AskQuestionForm";

import ScreenReaderModal from "./components/ScreenReaderModal";

export default function App() {
  const [showScreenReader, setShowScreenReader] = useState(false);

  return (
    <div className="app-root">
      {/* Header */}
      {/* Top Identity Bar (White) */}
      <header className="top-header">
        <div className="top-header-left">
          <img src={EvlLogo} alt="National Emblem" className="emblem" />
          <span className="govt-title">
            Unique Identification Authority of India
          </span>
        </div>

        <div className="top-header-right">
          <button
            className="utility-link"
            onClick={() => setShowScreenReader(true)}
          >
            Screen Reader
          </button>

          <span className="lang">English ▼</span>

          <img src={SiteLogo} alt="Aadhaar Logo" className="aadhaar-logo" />
        </div>
      </header>

      {/* App Header (Gradient) */}
      <header className="app-header">
        <span className="site-title">UIDAI HACKATHON 2026 (TEAMBOLT)</span>
      </header>

      {/* Content */}
      <main className="content">
        <>
          {/* KPI CARDS */}
          {/* KPI CARDS */}
          <div className="kpi-grid">
            {/* Volume */}
            <KpiCard title="Total Enrolments" value="1.45 Bn" icon={Users} />
            <KpiCard
              title="Total Demographic Updates"
              value="1.76 Bn"
              icon={FileText}
            />
            <KpiCard
              title="Total Biometric Updates"
              value="820 Mn"
              icon={Fingerprint}
            />

            {/* Performance */}
            <KpiCard
              title="Top Enrolment State"
              value="Uttar Pradesh"
              subtitle="12.4 Cr enrolments"
              icon={MapPin}
            />

            <KpiCard
              title="Top Update State"
              value="Maharashtra"
              subtitle="9.8 Cr updates"
              icon={TrendingUp}
            />

            <KpiCard
              title="Best Overall State"
              value="Tamil Nadu"
              subtitle="High enrolment & update ratio"
              icon={BarChart3}
            />

            {/* Saturation */}
            <KpiCard
              title="Saturated Enrolment State"
              value="Kerala"
              subtitle=">98% coverage"
              icon={AlertTriangle}
            />

            <KpiCard
              title="Saturated Update State"
              value="Delhi"
              subtitle="Low growth, high base"
              icon={AlertTriangle}
            />

            {/* New Enrolments by Age */}
            <KpiCard
              title="New Enrolments (Age 0–5)"
              value="3.2 Cr"
              subtitle="Child enrolments"
              icon={Baby}
            />

            <KpiCard
              title="New Enrolments (Age 5–17)"
              value="6.8 Cr"
              subtitle="School-age residents"
              icon={School}
            />

            <KpiCard
              title="New Enrolments (18+)"
              value="14.6 Cr"
              subtitle="Adult residents"
              icon={Users}
            />

            {/* Demographic Updates by Age */}
            <KpiCard
              title="Demographic Updates (Age 5–17)"
              value="4.1 Cr"
              subtitle="DOB, guardian, address"
              icon={FileText}
            />

            <KpiCard
              title="Demographic Updates (18+)"
              value="18.9 Cr"
              subtitle="Address, mobile, name"
              icon={FileText}
            />

            {/* Urban vs Rural */}
            <KpiCard
              title="Urban Update Share"
              value="62%"
              subtitle="Higher churn"
              icon={Building2}
            />

            <KpiCard
              title="Rural Update Share"
              value="38%"
              subtitle="Lower churn"
              icon={Home}
            />
          </div>

          {/* CHARTS */}
          <div className="grid">
            <AadhaarTrendChart
              title="Aadhaar Enrolment Trend"
              data={enrolmentTrendData}
              barColor="#6ec6ff"
            />

            <AadhaarTrendChart
              title="Aadhaar Update Trend"
              data={updateTrendData}
              barColor="#ff9e9e"
            />

            <UrbanRuralChurnPie
              title="Urban vs Rural Update Churn"
              urbanPercentage={62}
              ruralPercentage={38}
            />
          </div>

          {/* FAQ + ASK */}
          <div className="bottom-sections">
            <FaqSection />
            <AskQuestionForm />
          </div>
        </>
      </main>
      <ScreenReaderModal
        open={showScreenReader}
        onClose={() => setShowScreenReader(false)}
      />

      <footer className="footer">© UIDAI | Internal Analytics Dashboard</footer>
    </div>
  );
}
