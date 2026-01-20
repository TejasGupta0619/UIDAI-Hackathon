import type { LucideIcon } from "lucide-react";

type Props = {
  title: string;
  value: string;
  subtitle?: string;
  icon: LucideIcon;
};

export default function KpiCard({ title, value, subtitle, icon: Icon }: Props) {
  return (
    <div className="kpi-card">
      <div className="kpi-icon">
        <Icon size={22} />
      </div>

      <div className="kpi-content">
        <div className="kpi-value">{value}</div>
        <div className="kpi-title">{title}</div>
        {subtitle && <div className="kpi-subtitle">{subtitle}</div>}
      </div>
    </div>
  );
}
