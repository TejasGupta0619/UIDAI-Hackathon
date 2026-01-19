import React, { useState } from "react";
import {
  Upload,
  Play,
  Database,
  TrendingUp,
  Map,
  Users,
  Activity,
  FileText,
  Download,
} from "lucide-react";

const UidaiMLPipeline = () => {
  const [activeTab, setActiveTab] = useState("overview");
  const [pipelineStage, setPipelineStage] = useState("ready");

  const tabs = [
    { id: "overview", label: "Overview", icon: FileText },
    { id: "pipeline", label: "ML Pipeline", icon: Activity },
    { id: "features", label: "Feature Engineering", icon: Database },
    { id: "models", label: "Models & Tasks", icon: TrendingUp },
    { id: "implementation", label: "Implementation", icon: Play },
  ];

  const pipelineStages = [
    {
      name: "Data Loading",
      status: "complete",
      desc: "Load and merge all CSV files",
    },
    {
      name: "Preprocessing",
      status: "complete",
      desc: "Clean, encode, and transform data",
    },
    {
      name: "Feature Engineering",
      status: "complete",
      desc: "Create derived features and temporal patterns",
    },
    {
      name: "Train/Test Split",
      status: "complete",
      desc: "Temporal and spatial stratification",
    },
    {
      name: "Model Training",
      status: "ready",
      desc: "Train multiple ML models",
    },
    {
      name: "Evaluation",
      status: "pending",
      desc: "Validate and compare models",
    },
    {
      name: "Insights Generation",
      status: "pending",
      desc: "Extract actionable insights",
    },
  ];

  const mlTasks = [
    {
      task: "Enrollment Forecasting",
      type: "Regression",
      models: ["Random Forest", "XGBoost", "LSTM"],
      target: "Future enrollment counts by region",
      features: "Historical trends, demographics, seasonality",
    },
    {
      task: "Migration Detection",
      type: "Clustering",
      models: ["DBSCAN", "K-Means", "Hierarchical"],
      target: "Identify migration corridors",
      features: "Address update patterns, geographic data",
    },
    {
      task: "Anomaly Detection",
      type: "Unsupervised",
      models: ["Isolation Forest", "One-Class SVM", "Autoencoder"],
      target: "Unusual enrollment/update spikes",
      features: "Activity volume, temporal patterns",
    },
    {
      task: "Saturation Classification",
      type: "Classification",
      models: ["Gradient Boosting", "Random Forest"],
      target: "Predict region saturation level",
      features: "Enrollment rates, population density",
    },
    {
      task: "Biometric Quality Prediction",
      type: "Classification",
      models: ["XGBoost", "LightGBM"],
      target: "Predict regions needing re-capture",
      features: "Age distribution, update frequency",
    },
  ];

  const features = [
    {
      category: "Temporal Features",
      items: [
        "Day of week, month, quarter, year",
        "Days since first enrollment",
        "Rolling averages (7-day, 30-day)",
        "Lag features (previous week/month activity)",
        "Seasonal indicators (festival periods, school enrollment season)",
      ],
    },
    {
      category: "Geographic Features",
      items: [
        "PIN zone (first digit: 1-9)",
        "Urban/Rural classification from PIN",
        "State-level aggregations",
        "District-level density metrics",
        "Geographic clustering labels",
      ],
    },
    {
      category: "Demographic Features",
      items: [
        "Age group ratios (children vs adults)",
        "Update-to-enrollment ratio",
        "Biometric-to-demographic update ratio",
        "Average age profile per region",
        "Population coverage estimate",
      ],
    },
    {
      category: "Activity Features",
      items: [
        "Total activity volume (enroll + updates)",
        "Activity type distribution",
        "Activity velocity (rate of change)",
        "Peak activity timestamps",
        "Activity consistency score",
      ],
    },
    {
      category: "Derived Insights",
      items: [
        "Migration score (address update frequency)",
        "Saturation index (enrollment rate decline)",
        "Quality score (biometric update frequency)",
        "Government campaign indicators",
        "Socioeconomic proxies from patterns",
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-orange-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6 border-l-4 border-orange-500">
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                UIDAI Aadhaar Data Analysis Pipeline
              </h1>
              <p className="text-gray-600">
                Machine Learning Framework for Enrollment Trends, Migration
                Patterns & System Insights
              </p>
            </div>
            <div className="bg-gradient-to-r from-orange-500 to-blue-600 text-white px-4 py-2 rounded-lg">
              <div className="text-sm font-semibold">Hackathon Project</div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-xl shadow-lg mb-6 p-2">
          <div className="flex space-x-2">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg transition-all ${
                    activeTab === tab.id
                      ? "bg-gradient-to-r from-orange-500 to-blue-600 text-white shadow-md"
                      : "text-gray-600 hover:bg-gray-100"
                  }`}
                >
                  <Icon size={18} />
                  <span className="font-medium">{tab.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Content Area */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          {activeTab === "overview" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Project Overview
              </h2>

              <div className="grid md:grid-cols-3 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
                  <Database className="text-blue-600 mb-2" size={32} />
                  <h3 className="font-bold text-gray-900 mb-1">
                    3 Data Sources
                  </h3>
                  <p className="text-sm text-gray-700">
                    Enrollment, Demographic, Biometric updates
                  </p>
                </div>

                <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg border border-orange-200">
                  <Map className="text-orange-600 mb-2" size={32} />
                  <h3 className="font-bold text-gray-900 mb-1">
                    Geographic Coverage
                  </h3>
                  <p className="text-sm text-gray-700">
                    State, District, and PIN-level analysis
                  </p>
                </div>

                <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
                  <Users className="text-green-600 mb-2" size={32} />
                  <h3 className="font-bold text-gray-900 mb-1">
                    Age Segmentation
                  </h3>
                  <p className="text-sm text-gray-700">
                    0-5, 5-17, 18+ age groups
                  </p>
                </div>
              </div>

              <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
                <h3 className="font-bold text-gray-900 mb-3">Key Objectives</h3>
                <ul className="space-y-2 text-gray-700">
                  <li className="flex items-start gap-2">
                    <span className="text-orange-500 font-bold">•</span>
                    <span>
                      Identify enrollment saturation vs growth regions for
                      targeted campaigns
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-orange-500 font-bold">•</span>
                    <span>
                      Detect migration corridors through address update patterns
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-orange-500 font-bold">•</span>
                    <span>
                      Predict biometric quality issues for proactive re-capture
                      drives
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-orange-500 font-bold">•</span>
                    <span>
                      Forecast enrollment demand for resource allocation
                    </span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-orange-500 font-bold">•</span>
                    <span>
                      Uncover seasonal patterns and government campaign
                      effectiveness
                    </span>
                  </li>
                </ul>
              </div>

              <div className="bg-gradient-to-r from-orange-500 to-blue-600 text-white p-6 rounded-lg">
                <h3 className="font-bold mb-2 text-lg">Expected Outcomes</h3>
                <p className="text-sm opacity-90">
                  This pipeline will deliver actionable insights to support
                  UIDAI and Government of India in optimizing enrollment
                  centers, planning infrastructure, detecting fraud,
                  understanding demographic shifts, and improving service
                  delivery across India's massive Aadhaar ecosystem.
                </p>
              </div>
            </div>
          )}

          {activeTab === "pipeline" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                ML Pipeline Architecture
              </h2>

              <div className="space-y-3">
                {pipelineStages.map((stage, idx) => (
                  <div
                    key={idx}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      stage.status === "complete"
                        ? "bg-green-50 border-green-300"
                        : stage.status === "ready"
                          ? "bg-blue-50 border-blue-300"
                          : "bg-gray-50 border-gray-300"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold ${
                            stage.status === "complete"
                              ? "bg-green-500"
                              : stage.status === "ready"
                                ? "bg-blue-500"
                                : "bg-gray-400"
                          }`}
                        >
                          {idx + 1}
                        </div>
                        <div>
                          <h3 className="font-bold text-gray-900">
                            {stage.name}
                          </h3>
                          <p className="text-sm text-gray-600">{stage.desc}</p>
                        </div>
                      </div>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          stage.status === "complete"
                            ? "bg-green-200 text-green-800"
                            : stage.status === "ready"
                              ? "bg-blue-200 text-blue-800"
                              : "bg-gray-200 text-gray-600"
                        }`}
                      >
                        {stage.status.toUpperCase()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-lg border border-purple-200 mt-6">
                <h3 className="font-bold text-gray-900 mb-3">
                  Pipeline Design Principles
                </h3>
                <div className="grid md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <h4 className="font-semibold text-purple-800 mb-2">
                      Data Quality
                    </h4>
                    <ul className="space-y-1 text-gray-700">
                      <li>• Handle missing values and outliers</li>
                      <li>• Validate PIN codes and geographic data</li>
                      <li>• Remove duplicates and inconsistencies</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-purple-800 mb-2">
                      Scalability
                    </h4>
                    <ul className="space-y-1 text-gray-700">
                      <li>• Batch processing for large files</li>
                      <li>• Memory-efficient data structures</li>
                      <li>• Parallel processing where possible</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-purple-800 mb-2">
                      Validation
                    </h4>
                    <ul className="space-y-1 text-gray-700">
                      <li>• Time-based train/test split</li>
                      <li>• Cross-validation for robustness</li>
                      <li>• Geographic stratification</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-semibold text-purple-800 mb-2">
                      Reproducibility
                    </h4>
                    <ul className="space-y-1 text-gray-700">
                      <li>• Random seed for consistency</li>
                      <li>• Version control for models</li>
                      <li>• Pipeline configuration tracking</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "features" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Feature Engineering Strategy
              </h2>

              <div className="space-y-4">
                {features.map((category, idx) => (
                  <div
                    key={idx}
                    className="bg-gradient-to-r from-gray-50 to-white p-5 rounded-lg border border-gray-200"
                  >
                    <h3 className="font-bold text-gray-900 mb-3 text-lg">
                      {category.category}
                    </h3>
                    <ul className="space-y-2">
                      {category.items.map((item, itemIdx) => (
                        <li
                          key={itemIdx}
                          className="flex items-start gap-2 text-gray-700"
                        >
                          <span className="text-blue-500 font-bold mt-1">
                            →
                          </span>
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>

              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <h4 className="font-bold text-yellow-900 mb-2">
                  Feature Selection Strategy
                </h4>
                <p className="text-sm text-yellow-800">
                  Use correlation analysis, feature importance from tree models,
                  and domain knowledge to select the most predictive features.
                  Apply dimensionality reduction (PCA) for high-dimensional
                  feature spaces while maintaining interpretability.
                </p>
              </div>
            </div>
          )}

          {activeTab === "models" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                ML Tasks & Model Selection
              </h2>

              <div className="space-y-4">
                {mlTasks.map((task, idx) => (
                  <div
                    key={idx}
                    className="bg-white border-2 border-gray-200 rounded-lg p-5 hover:border-blue-400 transition-all"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="font-bold text-gray-900 text-lg">
                          {task.task}
                        </h3>
                        <span className="inline-block mt-1 px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full">
                          {task.type}
                        </span>
                      </div>
                    </div>

                    <div className="grid md:grid-cols-3 gap-4 mt-4">
                      <div>
                        <h4 className="font-semibold text-gray-700 text-sm mb-2">
                          Models
                        </h4>
                        <div className="flex flex-wrap gap-1">
                          {task.models.map((model, mIdx) => (
                            <span
                              key={mIdx}
                              className="px-2 py-1 bg-orange-100 text-orange-800 text-xs rounded"
                            >
                              {model}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-700 text-sm mb-2">
                          Target
                        </h4>
                        <p className="text-sm text-gray-600">{task.target}</p>
                      </div>

                      <div>
                        <h4 className="font-semibold text-gray-700 text-sm mb-2">
                          Features
                        </h4>
                        <p className="text-sm text-gray-600">{task.features}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-lg">
                <h3 className="font-bold mb-2 text-lg">
                  Model Evaluation Metrics
                </h3>
                <div className="grid md:grid-cols-3 gap-4 text-sm mt-3">
                  <div>
                    <h4 className="font-semibold mb-1">Regression</h4>
                    <p className="opacity-90">MAE, RMSE, R², MAPE</p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">Classification</h4>
                    <p className="opacity-90">
                      Accuracy, F1, Precision, Recall, ROC-AUC
                    </p>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-1">Clustering</h4>
                    <p className="opacity-90">
                      Silhouette, Davies-Bouldin, Calinski-Harabasz
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "implementation" && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Implementation Guide
              </h2>

              <div className="bg-gray-900 text-green-400 p-6 rounded-lg font-mono text-sm overflow-x-auto">
                <div className="mb-4 text-gray-400">
                  # Install required packages
                </div>
                <div>
                  pip install pandas numpy scikit-learn xgboost lightgbm
                  matplotlib seaborn
                </div>
              </div>

              <div className="space-y-4">
                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                  <h3 className="font-bold text-blue-900 mb-2">
                    Step 1: Data Loading & Merging
                  </h3>
                  <p className="text-sm text-blue-800">
                    Load all CSV chunks using pandas, concatenate them, and
                    merge the three datasets (enrollment, demographic,
                    biometric) on date, state, district, and pincode.
                  </p>
                </div>

                <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                  <h3 className="font-bold text-green-900 mb-2">
                    Step 2: Preprocessing
                  </h3>
                  <p className="text-sm text-green-800">
                    Convert date strings to datetime, encode categorical
                    variables (state, district), handle missing values, and
                    create the master feature matrix.
                  </p>
                </div>

                <div className="bg-purple-50 border-l-4 border-purple-500 p-4 rounded">
                  <h3 className="font-bold text-purple-900 mb-2">
                    Step 3: Feature Engineering
                  </h3>
                  <p className="text-sm text-purple-800">
                    Extract temporal features, create geographic encodings,
                    calculate ratios and aggregations, and generate derived
                    insights features.
                  </p>
                </div>

                <div className="bg-orange-50 border-l-4 border-orange-500 p-4 rounded">
                  <h3 className="font-bold text-orange-900 mb-2">
                    Step 4: Model Training
                  </h3>
                  <p className="text-sm text-orange-800">
                    Split data temporally, apply StandardScaler/MinMaxScaler,
                    train multiple models with cross-validation, and perform
                    hyperparameter tuning with GridSearchCV.
                  </p>
                </div>

                <div className="bg-pink-50 border-l-4 border-pink-500 p-4 rounded">
                  <h3 className="font-bold text-pink-900 mb-2">
                    Step 5: Evaluation & Insights
                  </h3>
                  <p className="text-sm text-pink-800">
                    Compare model performance, analyze feature importance,
                    generate visualizations, and extract actionable insights for
                    UIDAI decision-making.
                  </p>
                </div>
              </div>

              <div className="bg-gradient-to-r from-gray-800 to-gray-900 text-white p-6 rounded-lg">
                <h3 className="font-bold mb-3 text-lg flex items-center gap-2">
                  <Download size={20} />
                  Next Steps
                </h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    ✓ Review the complete Python implementation code artifact
                  </li>
                  <li>
                    ✓ Load your CSV files and run the preprocessing pipeline
                  </li>
                  <li>
                    ✓ Experiment with different models and hyperparameters
                  </li>
                  <li>✓ Generate visualizations and insight reports</li>
                  <li>
                    ✓ Prepare presentation with key findings for hackathon
                  </li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UidaiMLPipeline;
