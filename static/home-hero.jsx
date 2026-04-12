function ProgramHero({ logoUrl }) {
    const highlights = [
        "Leadership mentoring",
        "Hands-on summer projects",
        "Volunteer impact tracking"
    ];

    return (
        <section className="hero-shell">
            <img
                className="hero-logo"
                src={logoUrl}
                alt="Roman's Summer Bridge Program logo"
            />
            <p className="hero-kicker">Community. Growth. Bridge Building.</p>
            <h1 className="hero-title">Roman's Summer Bridge Program</h1>
            <p className="hero-subtitle">
                A place for students to connect, serve, and build momentum for the future.
            </p>

            <div className="hero-actions">
                <a href="/signup" className="hero-btn hero-btn-primary">Join the Program</a>
                <a href="/login" className="hero-btn hero-btn-ghost">Member Login</a>
            </div>

            <ul className="hero-highlights">
                {highlights.map((item) => (
                    <li key={item}>{item}</li>
                ))}
            </ul>
        </section>
    );
}

const heroRoot = document.getElementById("react-hero");
if (heroRoot) {
    const logoUrl = heroRoot.dataset.logoUrl || "/static/logo.png";
    const root = ReactDOM.createRoot(heroRoot);
    root.render(<ProgramHero logoUrl={logoUrl} />);
}
