
import { useState } from "react";
import {
  LayoutDashboard,
  Users,
  UserPlus,
  ClipboardList,
  Activity,
  Settings,
  LogOut,
  Bell,
  Menu,
  X
} from "lucide-react";

import "./Dashboard.css";

function Dashboard({ role = "Admin", staffName = "Staff Member" }) {
  const [activePage, setActivePage] = useState("Overview");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  
const roleMenus = {
  Admin: [
    { name: "Overview", icon: LayoutDashboard },
    { name: "Staff Management", icon: Users },
    { name: "Manage Roles", icon: Settings },
    { name: "Activity", icon: Activity },
    { name: "Settings", icon: Settings }
  ],

  Receptionist: [
    { name: "Overview", icon: LayoutDashboard },
    { name: "Patients", icon: Users },
    { name: "Register Patient", icon: UserPlus }
  ],

  Nurse: [
    { name: "Overview", icon: LayoutDashboard },
    { name: "Patients", icon: Users },
    { name: "Assessments", icon: ClipboardList },
    { name: "Vital Signs", icon: Activity },
    { name: "Medical History", icon: ClipboardList }
  ],

  Doctor: [
    { name: "Overview", icon: LayoutDashboard },
    { name: "Patients", icon: Users },
    { name: "Assessments", icon: ClipboardList },
    { name: "AI Triage Results", icon: Activity },
    { name: "Clinical Approval", icon: ClipboardList }
  ]
};

const menuItems = roleMenus[role] || roleMenus.Receptionist;


  return (
    <div className="dashboard-container">

      {/* Sidebar */}
      <aside className={`dashboard-sidebar ${sidebarOpen ? "sidebar-open" : ""}`}>

        <div className="dashboard-brand">
          <h2>IntelliTriage</h2>
          <span>SMARTER TRIAGE. BETTER CARE.</span>
        </div>

        <div className="dashboard-profile">
          <div className="profile-avatar">
            {staffName.charAt(0).toUpperCase()}
          </div>

          <div>
            <h4>{staffName}</h4>
            <p>{role}</p>
          </div>
        </div>

        <nav className="dashboard-menu">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.name}
                className={`dashboard-menu-item ${
                  activePage === item.name ? "active" : ""
                }`}
                onClick={() => {
                  setActivePage(item.name);
                  setSidebarOpen(false);
                }}
              >
                <Icon size={19} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </nav>

        <button className="dashboard-logout">
          <LogOut size={19} />
          <span>Logout</span>
        </button>

      </aside>

      {/* Main Content */}
      <main className="dashboard-main">

        <header className="dashboard-header">

          <button
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X /> : <Menu />}
          </button>

          <div>
            <h2>{activePage}</h2>
            <p>Welcome to your IntelliTriage workspace</p>
          </div>

          <button className="notification-button" aria-label="Notifications">
            <Bell size={21} />
          </button>

        </header>

        <section className="dashboard-content">

          <div className="dashboard-welcome">
            <div>
              <h1>Welcome back, {staffName}!</h1>
              <p>
                Your clinical workspace is ready.
                Manage your activities from here.
              </p>
            </div>
          </div>

          <div className="dashboard-stats">

            <div className="stat-card">
              <div className="stat-icon">
                <Users />
              </div>
              <h3>Patients</h3>
              <p>Patient management</p>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <ClipboardList />
              </div>
              <h3>Assessments</h3>
              <p>Clinical assessments</p>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <Activity />
              </div>
              <h3>Activities</h3>
              <p>Recent workspace activity</p>
            </div>

          </div>

          <div className="dashboard-information">
            <h2>{activePage}</h2>
            <p>
              This section will be developed according to your
              assigned staff role and approved project requirements.
            </p>
          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;
