import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

type Props = {
  title: string;
  urbanPercentage: number;
  ruralPercentage: number;
};

const COLORS = ["#4da3ff", "#9ccc65"]; // Urban, Rural (soft govt colors)

export default function UrbanRuralChurnPie({
  title,
  urbanPercentage,
  ruralPercentage,
}: Props) {
  const data = [
    { name: "Urban", value: urbanPercentage },
    { name: "Rural", value: ruralPercentage },
  ];

  return (
    <div className="chart-box">
      <div className="chart-header">{title}</div>

      <div className="chart-body">
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={90}
              label={({ name, value }) => `${name}: ${value}%`}
            >
              {data.map((_, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>

            <Tooltip formatter={(v: number | undefined) => `${v ?? 0}%`} />
            <Legend verticalAlign="bottom" height={36} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
