import { useState } from "react";
import {
  BarChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { BarChart3, TrendingUp, Download } from "lucide-react";

type Props = {
  title: string;
  data: any[];
  barColor: string;
};

export default function AadhaarTrendChart({ title, data, barColor }: Props) {
  const [showMonthly, setShowMonthly] = useState(true);
  const [showCumulative, setShowCumulative] = useState(true);

  const downloadCSV = () => {
    const headers = ["Month", "Monthly", "Cumulative"];
    const rows = data.map((d) => [d.month, d.monthly, d.cumulative].join(","));

    const csvContent =
      "data:text/csv;charset=utf-8," + [headers.join(","), ...rows].join("\n");

    const link = document.createElement("a");
    link.href = encodeURI(csvContent);
    link.download = `${title.replace(/\s+/g, "_")}.csv`;
    link.click();
  };

  return (
    <div className="chart-box large">
      <div className="chart-header">{title}</div>

      <div className="chart-body">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={data}
            margin={{ top: 20, right: 40, left: 40, bottom: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" tickMargin={10} />
            <YAxis yAxisId="left" tickMargin={10} />
            <YAxis yAxisId="right" orientation="right" tickMargin={10} />
            <Tooltip />

            {showMonthly && (
              <Bar
                yAxisId="left"
                dataKey="monthly"
                fill={barColor}
                name="Month Values"
              />
            )}

            {showCumulative && (
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="cumulative"
                stroke="#f5a623"
                dot={false}
                name="Cumulative Values"
              />
            )}
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Footer Controls */}
      <div className="chart-footer">
        <div className="chart-toggles">
          <button
            className={`icon-toggle ${showMonthly ? "active" : ""}`}
            onClick={() => setShowMonthly((v) => !v)}
            title="Toggle Month Values"
          >
            <BarChart3 size={18} />
          </button>

          <button
            className={`icon-toggle ${showCumulative ? "active" : ""}`}
            onClick={() => setShowCumulative((v) => !v)}
            title="Toggle Cumulative Values"
          >
            <TrendingUp size={18} />
          </button>
        </div>

        <button
          className="icon-toggle"
          onClick={downloadCSV}
          title="Download CSV"
        >
          <Download size={18} />
        </button>
      </div>
    </div>
  );
}
