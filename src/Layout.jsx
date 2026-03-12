import { NavLink, Outlet } from "react-router-dom";
import { theme, fontImports } from "./theme";

const navItems = [
  { to: "/", label: "每日 ArXiv 推荐", sub: "Daily ArXiv" },
  { to: "/graph", label: "科学发现图谱", sub: "Knowledge Graph" },
];

export default function Layout() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: theme.colors.background,
        fontFamily: theme.fonts.sans,
        display: "flex",
        flexDirection: "column",
        position: "relative",
      }}
    >
      <style>{`
        ${fontImports}
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: ${theme.colors.borderStrong}; border-radius: 6px; }
        a { text-decoration: none; color: inherit; }
        .tech-bg {
          position: absolute;
          inset: 0;
          pointer-events: none;
          background:
            linear-gradient(180deg, rgba(34, 211, 238, 0.03) 0%, transparent 50%),
            repeating-linear-gradient(0deg, transparent, transparent 24px, rgba(34, 211, 238, 0.04) 24px, rgba(34, 211, 238, 0.04) 25px),
            repeating-linear-gradient(90deg, transparent, transparent 24px, rgba(34, 211, 238, 0.04) 24px, rgba(34, 211, 238, 0.04) 25px);
        }
        input::placeholder { color: #64748b; }
      `}</style>
      <div className="tech-bg" aria-hidden="true" />

      <header
        style={{
          padding: "12px 24px",
          borderBottom: `1px solid ${theme.colors.border}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          background: `linear-gradient(180deg, ${theme.colors.surface} 0%, ${theme.colors.background} 100%)`,
          flexShrink: 0,
          zIndex: 20,
          position: "relative",
          boxShadow: `0 0 24px ${theme.colors.glow}08`,
        }}
      >
        <NavLink
          to="/"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 12,
            cursor: "pointer",
            transition: `opacity ${theme.transition}`,
          }}
          className={({ isActive }) => (isActive ? "active" : "")}
          onMouseEnter={(e) => (e.currentTarget.style.opacity = "0.85")}
          onMouseLeave={(e) => (e.currentTarget.style.opacity = "1")}
        >
          <div
            style={{
              width: 36,
              height: 36,
              borderRadius: theme.radius.md,
              background: `linear-gradient(135deg, ${theme.colors.cta}18, ${theme.colors.cta}30)`,
              border: `1px solid ${theme.colors.cta}`,
              boxShadow: `0 0 12px ${theme.colors.glow}`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke={theme.colors.cta} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
            </svg>
          </div>
          <div>
            <div style={{ fontFamily: theme.fonts.heading, color: theme.colors.primary, fontSize: 16, fontWeight: 600, letterSpacing: "0.08em" }}>
              科研日报
            </div>
            <div style={{ color: theme.colors.textSubtle, fontSize: 10, fontFamily: theme.fonts.mono, letterSpacing: "0.05em" }}>
              RESEARCH_DAILY
            </div>
          </div>
        </NavLink>

        <nav style={{ display: "flex", alignItems: "center", gap: 4 }}>
          {navItems.map(({ to, label, sub }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              style={({ isActive }) => ({
                padding: "10px 18px",
                borderRadius: theme.radius.md,
                fontFamily: theme.fonts.sans,
                fontSize: 14,
                fontWeight: 500,
                color: isActive ? theme.colors.cta : theme.colors.textMuted,
                background: isActive ? `${theme.colors.cta}15` : "transparent",
                border: isActive ? `1px solid ${theme.colors.borderStrong}` : "1px solid transparent",
                cursor: "pointer",
                transition: `color ${theme.transition}, background ${theme.transition}, border-color ${theme.transition}, box-shadow ${theme.transition}`,
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-start",
                lineHeight: 1.25,
                boxShadow: isActive ? `0 0 12px ${theme.colors.glow}30` : "none",
              })}
              onMouseEnter={(e) => {
                if (!e.currentTarget.classList.contains("active")) {
                  e.currentTarget.style.color = theme.colors.primary;
                  e.currentTarget.style.background = theme.colors.surface;
                  e.currentTarget.style.borderColor = theme.colors.border;
                }
              }}
              onMouseLeave={(e) => {
                if (!e.currentTarget.classList.contains("active")) {
                  e.currentTarget.style.color = theme.colors.textMuted;
                  e.currentTarget.style.background = "transparent";
                  e.currentTarget.style.borderColor = "transparent";
                }
              }}
            >
              <span>{label}</span>
              <span style={{ fontSize: 10, color: "inherit", opacity: 0.8 }}>{sub}</span>
            </NavLink>
          ))}
        </nav>
      </header>

      <main style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" }}>
        <Outlet />
      </main>
    </div>
  );
}
