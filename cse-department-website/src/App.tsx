import { useEffect, useState, type FormEvent, type ReactNode } from "react";
import {
  ArrowDownRight,
  ArrowRight,
  ArrowUp,
  ArrowUpRight,
  Award,
  BookOpen,
  BrainCircuit,
  Building2,
  BriefcaseBusiness,
  CalendarDays,
  Check,
  ChevronDown,
  Code2,
  ExternalLink,
  FileText,
  GraduationCap,
  Lightbulb,
  Mail,
  MapPin,
  Menu,
  Microscope,
  Network,
  Search,
  ShieldCheck,
  Sparkles,
  Users,
  X,
} from "lucide-react";
import { motion, useReducedMotion } from "framer-motion";
import {
  Link,
  NavLink,
  Route,
  Routes,
  useLocation,
  useParams,
} from "react-router-dom";
import {
  achievements,
  clubs,
  courses,
  events,
  faculty,
  notices,
  projectCategories,
  projects,
  researchAreas,
} from "./data";

const heroImage =
  "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=2200&q=90";
const campusImage =
  "https://images.unsplash.com/photo-1562774053-701939374585?auto=format&fit=crop&w=1400&q=85";

const exploreLinks = [
  { to: "/faculty", label: "Faculty" },
  { to: "/research", label: "Research & innovation" },
  { to: "/projects", label: "Student projects" },
  { to: "/events", label: "Events" },
  { to: "/achievements", label: "Achievements" },
  { to: "/student-life", label: "Student life" },
  { to: "/careers", label: "Careers" },
];

function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "auto" });
  }, [pathname]);

  return null;
}

function Reveal({ children, className = "" }: { children: ReactNode; className?: string }) {
  const reducedMotion = useReducedMotion();
  return (
    <motion.div
      className={className}
      initial={reducedMotion ? false : { opacity: 0, y: 18 }}
      whileInView={reducedMotion ? undefined : { opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.14 }}
      transition={{ duration: 0.48, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}

function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [exploreOpen, setExploreOpen] = useState(false);
  const closeMenu = () => {
    setMobileOpen(false);
    setExploreOpen(false);
  };

  return (
    <>
      <a className="skip-link" href="#main-content">Skip to content</a>
      <div className="utility-bar">
        <div className="container utility-inner">
          <span>BMS Institute of Technology &amp; Management</span>
          <span className="utility-note">A digital home for curious minds</span>
        </div>
      </div>
      <header className="site-header">
        <div className="container header-inner">
          <Link className="brand" to="/" onClick={closeMenu} aria-label="CSE department home">
            <span className="brand-mark" aria-hidden="true">
              <span />
              <span />
              <span />
            </span>
            <span className="brand-copy">
              <strong>BMSIT&amp;M</strong>
              <small>COMPUTER SCIENCE &amp; ENGINEERING</small>
            </span>
          </Link>
          <button
            className="mobile-menu-button"
            type="button"
            aria-label={mobileOpen ? "Close navigation" : "Open navigation"}
            aria-expanded={mobileOpen}
            aria-controls="primary-navigation"
            onClick={() => setMobileOpen((open) => !open)}
          >
            {mobileOpen ? <X size={21} /> : <Menu size={21} />}
          </button>
          <nav
            id="primary-navigation"
            className={`main-nav${mobileOpen ? " is-open" : ""}`}
            aria-label="Main navigation"
          >
            <NavLink to="/" end className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} onClick={closeMenu}>
              Home
            </NavLink>
            <NavLink to="/about" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} onClick={closeMenu}>
              About
            </NavLink>
            <NavLink to="/academics" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} onClick={closeMenu}>
              Academics
            </NavLink>
            <div className="nav-dropdown">
              <button
                type="button"
                className={`nav-link dropdown-trigger${exploreOpen ? " active" : ""}`}
                aria-expanded={exploreOpen}
                aria-controls="explore-menu"
                onClick={() => setExploreOpen((open) => !open)}
              >
                Explore <ChevronDown size={14} />
              </button>
              <div id="explore-menu" className={`dropdown-menu${exploreOpen ? " is-open" : ""}`}>
                {exploreLinks.map((item) => (
                  <Link key={item.to} to={item.to} onClick={closeMenu}>
                    {item.label}<ArrowUpRight size={14} />
                  </Link>
                ))}
              </div>
            </div>
            <NavLink to="/notices" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} onClick={closeMenu}>
              Notices
            </NavLink>
            <NavLink to="/contact" className={({ isActive }) => `nav-link${isActive ? " active" : ""}`} onClick={closeMenu}>
              Contact
            </NavLink>
            <Link className="nav-cta" to="/projects" onClick={closeMenu}>
              See what we build <ArrowUpRight size={15} />
            </Link>
          </nav>
        </div>
      </header>
      <div className="demo-ribbon" role="note">
        <span className="demo-ribbon-dot" />
        Website concept · All sample people, events and curriculum are illustrative and need verification
      </div>
    </>
  );
}

function Footer() {
  return (
    <footer className="site-footer">
      <div className="container footer-main">
        <div className="footer-brand">
          <Link className="brand brand-light" to="/">
            <span className="brand-mark" aria-hidden="true"><span /><span /><span /></span>
            <span className="brand-copy">
              <strong>BMSIT&amp;M</strong>
              <small>COMPUTER SCIENCE &amp; ENGINEERING</small>
            </span>
          </Link>
          <p>A considered digital space for learning, research, collaboration, and ideas in computing.</p>
        </div>
        <div className="footer-column">
          <h3>Discover</h3>
          <Link to="/about">About the department</Link>
          <Link to="/academics">Academics</Link>
          <Link to="/faculty">Faculty directory</Link>
          <Link to="/research">Research &amp; innovation</Link>
        </div>
        <div className="footer-column">
          <h3>Community</h3>
          <Link to="/projects">Student projects</Link>
          <Link to="/events">Events &amp; activities</Link>
          <Link to="/student-life">Student life</Link>
          <Link to="/careers">Career resources</Link>
        </div>
        <div className="footer-contact">
          <span className="footer-eyebrow">Have a question?</span>
          <p>Official department contact details are awaiting verification.</p>
          <Link className="footer-contact-link" to="/contact">Visit contact page <ArrowRight size={15} /></Link>
        </div>
      </div>
      <div className="container footer-bottom">
        <span>© {new Date().getFullYear()} BMSIT&amp;M CSE · Website concept</span>
        <span>Sample content is clearly marked and should be verified before publication.</span>
      </div>
    </footer>
  );
}

function BackToTop() {
  const [visible, setVisible] = useState(false);
  useEffect(() => {
    const updateVisibility = () => setVisible(window.scrollY > 420);
    updateVisibility();
    window.addEventListener("scroll", updateVisibility, { passive: true });
    return () => window.removeEventListener("scroll", updateVisibility);
  }, []);

  if (!visible) return null;
  return (
    <button
      className="back-to-top"
      type="button"
      aria-label="Back to top"
      onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
    >
      <ArrowUp size={18} />
    </button>
  );
}

function SiteLayout() {
  return (
    <>
      <ScrollToTop />
      <Header />
      <main id="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/academics" element={<AcademicsPage />} />
          <Route path="/faculty" element={<FacultyPage />} />
          <Route path="/faculty/:id" element={<FacultyDetailPage />} />
          <Route path="/research" element={<ResearchPage />} />
          <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/projects/:id" element={<ProjectDetailPage />} />
          <Route path="/events" element={<EventsPage />} />
          <Route path="/events/:id" element={<EventDetailPage />} />
          <Route path="/achievements" element={<AchievementsPage />} />
          <Route path="/student-life" element={<StudentLifePage />} />
          <Route path="/careers" element={<CareersPage />} />
          <Route path="/notices" element={<NoticesPage />} />
          <Route path="/notices/:id" element={<NoticeDetailPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
      <Footer />
      <BackToTop />
    </>
  );
}

function SectionHeading({
  eyebrow,
  title,
  description,
  link,
}: {
  eyebrow: string;
  title: string;
  description?: string;
  link?: { to: string; label: string };
}) {
  return (
    <div className="section-heading">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h2>{title}</h2>
        {description && <p>{description}</p>}
      </div>
      {link && <Link className="text-link" to={link.to}>{link.label}<ArrowRight size={16} /></Link>}
    </div>
  );
}

function PageHero({
  eyebrow,
  title,
  description,
  image,
}: {
  eyebrow: string;
  title: string;
  description: string;
  image?: string;
}) {
  return (
    <section className={`page-hero${image ? " page-hero-image" : ""}`} style={image ? { backgroundImage: `linear-gradient(90deg, rgba(16,36,58,.94), rgba(16,36,58,.76) 56%, rgba(16,36,58,.38)), url("${image}")` } : undefined}>
      <div className="container page-hero-content">
        <span className="eyebrow eyebrow-light">{eyebrow}</span>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
    </section>
  );
}

function SampleNote({ children = "Illustrative content · Replace with verified department information before publishing" }: { children?: ReactNode }) {
  return <p className="sample-note"><span className="sample-note-mark">i</span>{children}</p>;
}

function HomePage() {
  const highlights = [
    { icon: BookOpen, label: "Learn deeply", title: "An education built on foundations", text: "Explore a sample view of core computing, practical studios, and a curriculum that grows with the field.", to: "/academics", number: "01" },
    { icon: Microscope, label: "Ask better questions", title: "Research with curiosity", text: "Discover possible areas of inquiry across intelligent systems, data, security, and software.", to: "/research", number: "02" },
    { icon: Lightbulb, label: "Make something matter", title: "Ideas become working prototypes", text: "Browse demonstration projects that show how student work can be shared with context.", to: "/projects", number: "03" },
  ];

  return (
    <>
      <section className="home-hero">
        <img className="home-hero-image" src={heroImage} alt="Students collaborating around a computer in a bright studio" fetchPriority="high" />
        <div className="home-hero-overlay" />
        <div className="container home-hero-content">
          <div className="hero-copy">
            <div className="hero-kicker"><span /> COMPUTER SCIENCE &amp; ENGINEERING <span className="hero-kicker-line" /></div>
            <h1>Engineering the future <em>through computing.</em></h1>
            <p>Explore knowledge, build solutions, and shape the future of technology through Computer Science and Engineering.</p>
            <div className="hero-actions">
              <Link className="button button-light" to="/about">Explore our department <ArrowRight size={16} /></Link>
              <Link className="button button-outline-light" to="/projects">Discover student projects <ArrowUpRight size={16} /></Link>
            </div>
          </div>
          <div className="hero-aside">
            <span className="hero-aside-index">BMSIT&amp;M / CSE</span>
            <span className="hero-aside-rule" />
            <p>A place for questions, careful thinking, and the next bright idea.</p>
            <Link to="/student-life" aria-label="Explore student life"><ArrowDownRight size={20} /></Link>
          </div>
          <div className="hero-caption"><span>LEARN WITH PURPOSE</span><span>BUILD WITH CARE</span><span>SHARE WHAT YOU DISCOVER</span></div>
        </div>
        <div className="hero-index">BENGALURU <span>·</span> INDIA</div>
      </section>

      <section className="intro-section section-pad">
        <div className="container intro-grid">
          <div className="intro-index"><span>01</span><span className="vertical-rule" /> A DEPARTMENT IN MOTION</div>
          <div className="intro-copy">
            <Reveal>
              <span className="eyebrow">Computing is a way to ask what if</span>
              <h2>Make room for <em>big questions.</em></h2>
              <p className="intro-lead">Computer Science is more than code. It is the craft of understanding complex ideas, designing useful systems, and creating technology with people in mind.</p>
              <Link className="text-link" to="/about">Get to know the department <ArrowRight size={16} /></Link>
            </Reveal>
          </div>
          <div className="intro-image-wrap">
            <img src={campusImage} alt="Modern university building framed by green trees" loading="lazy" />
            <div className="image-caption"><span>PLACE TO THINK, MAKE &amp; GROW</span><ArrowUpRight size={17} /></div>
          </div>
        </div>
      </section>

      <section className="highlight-section section-pad">
        <div className="container">
          <SectionHeading eyebrow="A connected experience" title="Learn. Explore. Create." description="A department experience shaped around ideas, practice, and community." />
          <div className="highlight-grid">
            {highlights.map((item) => (
              <Reveal key={item.number} className="highlight-reveal">
                <Link className="highlight-card" to={item.to}>
                  <div className="highlight-card-top"><span className="highlight-icon"><item.icon size={21} /></span><span className="card-number">{item.number}</span></div>
                  <span className="highlight-label">{item.label}</span>
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                  <span className="card-arrow"><ArrowUpRight size={18} /></span>
                </Link>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="quote-band">
        <div className="container quote-inner">
          <span className="eyebrow eyebrow-light">OUR POINT OF VIEW</span>
          <p>“Good technology begins with understanding the world it enters.”</p>
          <span className="quote-caption">A guiding thought for this department website concept</span>
        </div>
      </section>

      <section className="projects-preview section-pad">
        <div className="container">
          <SectionHeading eyebrow="From the student studio" title="A glimpse of what we could build." description="Demonstration project cards, ready to be replaced with real student work." link={{ to: "/projects", label: "View all projects" }} />
          <div className="project-grid">
            {projects.slice(0, 3).map((project, index) => <ProjectCard key={project.id} project={project} index={index} />)}
          </div>
        </div>
      </section>

      <section className="pathway-section">
        <div className="container pathway-grid">
          <div className="pathway-image"><img src="https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=85" alt="Students sharing ideas together on campus" loading="lazy" /></div>
          <div className="pathway-copy">
            <span className="eyebrow eyebrow-light">Make your next move</span>
            <h2>Find your place in the story.</h2>
            <p>Whether you are exploring a degree, looking for collaborators, or curious about a research idea, there is a starting point here.</p>
            <div className="pathway-links">
              <Link to="/academics"><GraduationCap size={19} /><span>Explore academics</span><ArrowUpRight size={16} /></Link>
              <Link to="/student-life"><Users size={19} /><span>Meet student communities</span><ArrowUpRight size={16} /></Link>
              <Link to="/contact"><Mail size={19} /><span>Connect with the department</span><ArrowUpRight size={16} /></Link>
            </div>
          </div>
        </div>
      </section>

      <section className="notice-preview section-pad">
        <div className="container">
          <SectionHeading eyebrow="Stay in the loop" title="From the notice board." description="Sample updates demonstrate how academic and community notices can be shared." link={{ to: "/notices", label: "Open notice board" }} />
          <div className="notice-preview-list">
            {notices.slice(0, 3).map((notice) => (
              <Link className="notice-preview-row" key={notice.id} to={`/notices/${notice.id}`}>
                <span className="notice-date">{formatDate(notice.date)}</span>
                <span className="notice-category">{notice.category}</span>
                <span className="notice-title">{notice.title}</span>
                <ArrowUpRight size={18} />
              </Link>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}

function AboutPage() {
  const pillars = [
    ["01", "Understand before building", "Learn to frame problems carefully and approach complexity with patience."],
    ["02", "Build with people in mind", "Connect technical choices to the needs, contexts, and experiences of real communities."],
    ["03", "Keep learning together", "Make room for experimentation, constructive critique, and ideas that cross disciplines."],
  ];
  return (
    <>
      <PageHero eyebrow="About the department" title="Computing with purpose." description="A place to develop strong foundations, explore emerging ideas, and create technology thoughtfully." image={campusImage} />
      <section className="section-pad">
        <div className="container about-intro-grid">
          <div className="about-stamp"><span>BMSIT&amp;M</span><strong>CSE</strong><span>BENGALURU · INDIA</span></div>
          <div className="about-copy">
            <span className="eyebrow">A department overview</span>
            <h2>Where fundamentals meet possibility.</h2>
            <p className="intro-lead">This department website is designed as a digital hub for students, faculty, alumni, prospective students, researchers, and collaborators.</p>
            <p>Its editorial direction brings together learning, research, student work, and community. The department's verified history, programme details, facilities, and official statements can be added here when approved information is available.</p>
            <SampleNote>Overview and statements on this page are conceptual; they are not official institutional claims.</SampleNote>
          </div>
        </div>
      </section>
      <section className="about-vision section-pad">
        <div className="container vision-grid">
          <div><span className="eyebrow eyebrow-light">A thoughtful starting point</span><h2>Curiosity is a <em>practice.</em></h2></div>
          <div><p>Rather than invent official vision or mission language, this concept leaves those statements open for the department to supply and approve.</p><div className="statement-placeholder"><span>VISION</span><p>Official vision statement to be added after verification.</p></div><div className="statement-placeholder"><span>MISSION</span><p>Official mission statement to be added after verification.</p></div></div>
        </div>
      </section>
      <section className="section-pad">
        <div className="container">
          <SectionHeading eyebrow="How we approach learning" title="A few useful principles." description="Conceptual principles for the design of this experience, not official departmental statements." />
          <div className="pillar-list">{pillars.map(([number, title, text]) => <div className="pillar-row" key={number}><span>{number}</span><h3>{title}</h3><p>{text}</p></div>)}</div>
        </div>
      </section>
      <section className="section-pad about-facilities">
        <div className="container about-facilities-grid">
          <div><span className="eyebrow">Learning environment</span><h2>Space for the work behind the work.</h2><p>Lab facilities, infrastructure, industry connections, and programme outcomes should be described using verified department information. This section is intentionally kept factual and ready for that content.</p><Link className="text-link" to="/academics">Explore the academic experience <ArrowRight size={16} /></Link></div>
          <img src="https://images.unsplash.com/photo-1581092921461-eab62e97a780?auto=format&fit=crop&w=1200&q=85" alt="A bright technology lab with workstations" loading="lazy" />
        </div>
      </section>
      <section className="section-pad">
        <div className="container">
          <SectionHeading eyebrow="Ready for verified detail" title="The foundations behind the experience." description="These areas are intentionally left open until the department can provide confirmed information." />
          <div className="about-detail-grid">
            <article><span className="about-detail-number">01</span><Building2 size={21} /><h3>Infrastructure</h3><p>Confirmed laboratories, equipment, learning spaces, and facility information to be added.</p></article>
            <article><span className="about-detail-number">02</span><Network size={21} /><h3>Industry connections</h3><p>Verified collaborations, guest engagements, and partnership details to be added.</p></article>
          </div>
        </div>
      </section>
    </>
  );
}

function AcademicsPage() {
  const [semester, setSemester] = useState(1);
  const semesterCourses = courses.filter((course) => course.semester === semester);
  return (
    <>
      <PageHero eyebrow="Academics" title="A strong foundation. A wider horizon." description="Explore a sample undergraduate computing pathway and an interactive curriculum preview." />
      <section className="section-pad">
        <div className="container">
          <SampleNote>This curriculum is illustrative sample data, not the approved BMSIT&amp;M syllabus. Course codes, credits, and outcomes must be verified.</SampleNote>
          <div className="program-intro">
            <div className="program-icon"><GraduationCap size={26} /></div>
            <div><span className="eyebrow">Undergraduate programme</span><h2>B.E. Computer Science and Engineering</h2><p>Explore the foundations of computation, software, systems, and problem-solving through a sample semester-based curriculum.</p></div>
            <span className="program-label">Programme overview · sample</span>
          </div>
          <div className="curriculum-wrap">
            <div className="curriculum-heading"><div><span className="eyebrow">Curriculum explorer</span><h2>Choose a semester.</h2></div><span className="curriculum-caption">8 SEMESTERS · SAMPLE VIEW</span></div>
            <div className="semester-tabs" role="tablist" aria-label="Select semester">
              {Array.from({ length: 8 }, (_, index) => index + 1).map((number) => (
                <button key={number} id={`semester-tab-${number}`} type="button" role="tab" aria-selected={semester === number} aria-controls="semester-courses" className={semester === number ? "semester-tab active" : "semester-tab"} onClick={() => setSemester(number)}>S{number}</button>
              ))}
            </div>
            <div className="course-list" id="semester-courses" role="tabpanel" aria-labelledby={`semester-tab-${semester}`}>
              {semesterCourses.map((course, index) => (
                <article className="course-row" key={course.code}>
                  <span className="course-index">0{index + 1}</span><div className="course-main"><h3>{course.name}</h3><span>{course.code}</span></div><span className="course-type">{course.type}</span><span className="course-credits">{course.credits}<small>credits · sample</small></span>
                </article>
              ))}
              <div className="course-footnote"><FileText size={16} /><span>Approved course outlines and downloadable syllabi are not available in this demo.</span></div>
            </div>
          </div>
          <div className="outcomes-grid">
            {[
              ["Programme structure", "Add approved course structure and academic regulations."],
              ["Learning outcomes", "Add verified programme outcomes and learning objectives."],
              ["Labs & facilities", "Add confirmed laboratory and infrastructure information."],
            ].map(([title, text]) => <article className="outcome-card" key={title}><span className="outcome-icon"><BookOpen size={19} /></span><h3>{title}</h3><p>{text}</p></article>)}
          </div>
        </div>
      </section>
    </>
  );
}

function FacultyPage() {
  const [query, setQuery] = useState("");
  const [designation, setDesignation] = useState("All designations");
  const [specialization, setSpecialization] = useState("All specializations");
  const designations = Array.from(new Set(faculty.map((person) => person.role)));
  const specializations = Array.from(new Set(faculty.map((person) => person.expertise)));
  const filtered = faculty.filter((person) => {
    const text = `${person.name} ${person.role} ${person.expertise} ${person.focus}`.toLowerCase();
    return text.includes(query.toLowerCase())
      && (designation === "All designations" || person.role === designation)
      && (specialization === "All specializations" || person.expertise === specialization);
  });
  return (
    <>
      <PageHero eyebrow="Faculty" title="People who make ideas grow." description="A thoughtful faculty directory experience, ready for verified profiles and research expertise." />
      <section className="section-pad">
        <div className="container">
          <SampleNote>These are clearly marked placeholder profiles. No real faculty identity, designation, qualification, or contact detail is represented.</SampleNote>
          <div className="filter-toolbar">
            <label className="search-field"><Search size={18} /><input type="search" placeholder="Search faculty or interests" value={query} onChange={(event) => setQuery(event.target.value)} /><span className="sr-only">Search faculty</span></label>
            <label className="select-field"><span className="sr-only">Filter by designation</span><select value={designation} onChange={(event) => setDesignation(event.target.value)}><option>All designations</option>{designations.map((item) => <option key={item}>{item}</option>)}</select></label>
            <label className="select-field"><span className="sr-only">Filter by specialization</span><select value={specialization} onChange={(event) => setSpecialization(event.target.value)}><option>All specializations</option>{specializations.map((item) => <option key={item}>{item}</option>)}</select></label>
          </div>
          <p className="result-count">Showing {filtered.length} sample {filtered.length === 1 ? "profile" : "profiles"}</p>
          <div className="faculty-grid">{filtered.map((person, index) => <FacultyCard key={person.id} person={person} index={index} />)}</div>
          {filtered.length === 0 && <EmptyState title="No profiles match those filters." text="Try another search or reset the filters." />}
        </div>
      </section>
    </>
  );
}

function FacultyCard({ person, index }: { person: (typeof faculty)[number]; index: number }) {
  const initials = `D${String(index + 1).padStart(2, "0")}`;
  return (
    <Reveal className="faculty-reveal">
      <article className="faculty-card">
        <div className={`faculty-avatar avatar-${index % 4}`} aria-hidden="true"><span>{initials}</span><div className="avatar-orbit" /></div>
        <div className="faculty-card-body"><span className="faculty-role">{person.role}</span><h3>{person.name}</h3><p className="faculty-expertise">{person.expertise}</p><p>{person.focus}</p><Link className="text-link" to={`/faculty/${person.id}`}>View sample profile <ArrowRight size={15} /></Link></div>
      </article>
    </Reveal>
  );
}

function FacultyDetailPage() {
  const { id } = useParams();
  const person = faculty.find((item) => item.id === id);
  if (!person) return <NotFoundPage />;
  return (
    <>
      <PageHero eyebrow="Faculty · sample profile" title={person.name} description={person.expertise} />
      <section className="section-pad"><div className="container detail-layout"><div className="detail-back"><Link className="text-link" to="/faculty"><ArrowRight className="back-arrow" size={16} /> Back to faculty directory</Link></div><div className="detail-main"><SampleNote>Profile placeholder. Replace all fields with verified information and obtain consent before publishing.</SampleNote><h2>{person.role}</h2><p className="intro-lead">{person.focus}</p><div className="detail-info-grid"><div><span>Research interests</span><strong>{person.expertise}</strong></div><div><span>Education</span><strong>Information to be confirmed</strong></div><div><span>Publications &amp; projects</span><strong>Verified details to be added</strong></div><div><span>Contact</span><strong>Official contact details not supplied</strong></div></div></div></div></section>
    </>
  );
}

function ResearchPage() {
  const areas = [
    { icon: BrainCircuit, title: researchAreas[0], note: "Possible area · editable" },
    { icon: Network, title: researchAreas[1], note: "Possible area · editable" },
    { icon: ShieldCheck, title: researchAreas[2], note: "Possible area · editable" },
    { icon: Lightbulb, title: researchAreas[3], note: "Possible area · editable" },
    { icon: Search, title: researchAreas[4], note: "Possible area · editable" },
    { icon: Code2, title: researchAreas[5], note: "Possible area · editable" },
    { icon: Sparkles, title: researchAreas[6], note: "Possible area · editable" },
    { icon: Network, title: researchAreas[7], note: "Possible area · editable" },
  ];
  return (
    <>
      <PageHero eyebrow="Research & innovation" title="Questions worth exploring." description="A window into possible research directions, student inquiry, and collaboration." image="https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=1800&q=85" />
      <section className="section-pad"><div className="container"><SampleNote>These are possible computing research areas, not claims about active or officially recognised department research groups.</SampleNote><SectionHeading eyebrow="Possible research areas" title="Many directions. Shared curiosity." description="Editable topic cards to be aligned with verified faculty research and active laboratories." /><div className="research-area-grid">{areas.map(({ icon: Icon, title, note }, index) => <Reveal key={title}><article className="research-area-card"><span className="research-count">0{index + 1}</span><Icon size={22} strokeWidth={1.7} /><h3>{title}</h3><p>{note}</p></article></Reveal>)}</div></div></section>
      <section className="research-feature"><div className="container research-feature-grid"><div className="research-feature-art"><span className="feature-orbit orbit-one" /><span className="feature-orbit orbit-two" /><span className="feature-orbit orbit-three" /><span className="feature-core"><Microscope size={31} /></span><span className="feature-chip chip-one">IDEA</span><span className="feature-chip chip-two">TEST</span><span className="feature-chip chip-three">SHARE</span></div><div><span className="eyebrow eyebrow-light">From question to contribution</span><h2>Research is a conversation.</h2><p>Faculty projects, publications, student research, facilities, and industry collaborations can be introduced here once their information and permissions are confirmed.</p><div className="research-feature-links"><Link to="/faculty">Meet the faculty <ArrowRight size={15} /></Link><Link to="/projects">Explore sample projects <ArrowRight size={15} /></Link></div></div></div></section>
      <section className="section-pad"><div className="container research-pillars">{[["Faculty research", "Verified profiles, projects, and publication links."], ["Student inquiry", "Research posters, capstones, and student-led investigations."], ["Collaborations", "Confirmed partnerships, labs, and innovation programmes."]].map(([title, text]) => <article key={title}><span className="eyebrow">To be developed</span><h3>{title}</h3><p>{text}</p></article>)}</div></section>
    </>
  );
}

function ProjectCard({ project, index = 0 }: { project: (typeof projects)[number]; index?: number }) {
  return (
    <Reveal className="project-reveal">
      <Link to={`/projects/${project.id}`} className={`project-card${index === 0 ? " project-card-featured" : ""}`}>
        <div className="project-image-wrap"><img src={project.image} alt="" loading="lazy" /><span className="project-index">0{index + 1}</span><span className="project-image-arrow"><ArrowUpRight size={18} /></span></div>
        <div className="project-card-body"><div className="project-meta"><span>{project.category}</span><span>{project.status}</span></div><h3>{project.title}</h3><p>{project.description}</p><div className="tag-row">{project.stack.map((item) => <span className="tag" key={item}>{item}</span>)}</div></div>
      </Link>
    </Reveal>
  );
}

function ProjectsPage() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");
  const filteredProjects = projects.filter((project) => {
    const matchesText = `${project.title} ${project.description} ${project.stack.join(" ")}`.toLowerCase().includes(query.toLowerCase());
    return matchesText && (category === "All" || project.category === category);
  });
  return (
    <>
      <PageHero eyebrow="Student projects" title="Ideas, made tangible." description="A searchable showcase concept for student work, prototypes, and team projects." image="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1800&q=85" />
      <section className="section-pad"><div className="container"><SampleNote>All projects shown are demonstration content; teams, technologies, and links are fictional examples.</SampleNote><div className="section-heading project-heading"><div><span className="eyebrow">The project gallery</span><h2>Made by curious minds.</h2></div><p className="gallery-description">Use the filters to find work by theme. Open any card for a sample project detail.</p></div><div className="project-filters"><label className="search-field"><Search size={18} /><input type="search" placeholder="Search projects" value={query} onChange={(event) => setQuery(event.target.value)} /><span className="sr-only">Search projects</span></label><div className="filter-chips" aria-label="Filter projects by category">{projectCategories.map((item) => <button type="button" key={item} className={category === item ? "filter-chip active" : "filter-chip"} aria-pressed={category === item} onClick={() => setCategory(item)}>{item}</button>)}</div></div><p className="result-count">{filteredProjects.length} demonstration {filteredProjects.length === 1 ? "project" : "projects"}</p><div className="project-grid">{filteredProjects.map((project, index) => <ProjectCard key={project.id} project={project} index={index} />)}</div>{filteredProjects.length === 0 && <EmptyState title="No projects found." text="Try a different search or category." />}</div></section>
    </>
  );
}

function ProjectDetailPage() {
  const { id } = useParams();
  const project = projects.find((item) => item.id === id);
  if (!project) return <NotFoundPage />;
  return (
    <>
      <PageHero eyebrow={`${project.category} · project sample`} title={project.title} description={project.description} image={project.image} />
      <section className="section-pad"><div className="container detail-layout"><div className="detail-back"><Link className="text-link" to="/projects"><ArrowRight className="back-arrow" size={16} /> Back to projects</Link></div><div className="detail-main"><SampleNote>This is a demonstration project. No GitHub repository, live demo, or real team information is implied.</SampleNote><div className="detail-info-grid"><div><span>Category</span><strong>{project.category}</strong></div><div><span>Team</span><strong>{project.team}</strong></div><div><span>Project status</span><strong>{project.status}</strong></div><div><span>Technology</span><strong>{project.stack.join(" · ")}</strong></div></div><h2>About this concept</h2><p className="intro-lead">{project.description} This detail view shows how a verified project story could describe the challenge, approach, and what the team learned.</p><Link className="button button-navy" to="/contact">Ask about showcasing a project <ArrowRight size={16} /></Link></div></div></section>
    </>
  );
}

function EventCard({ event }: { event: (typeof events)[number] }) {
  return (
    <Link className="event-card" to={`/events/${event.id}`}>
      <div className="event-date-block"><span>{new Date(`${event.date}T12:00:00`).toLocaleDateString("en", { month: "short" })}</span><strong>{new Date(`${event.date}T12:00:00`).getDate()}</strong><small>{new Date(`${event.date}T12:00:00`).getFullYear()}</small></div>
      <div className="event-card-content"><div className="event-topline"><span>{event.type}</span><span>SAMPLE EVENT</span></div><h3>{event.title}</h3><p>{event.description}</p><span className="event-venue"><MapPin size={14} />{event.venue}</span></div>
      <span className="event-arrow"><ArrowUpRight size={18} /></span>
    </Link>
  );
}

function EventsPage() {
  const [period, setPeriod] = useState("All events");
  const [type, setType] = useState("All types");
  const [query, setQuery] = useState("");
  const today = new Date().toISOString().slice(0, 10);
  const eventTypes = Array.from(new Set(events.map((event) => event.type)));
  const filtered = events.filter((event) => {
    const isUpcoming = event.date >= today;
    return (period === "All events" || (period === "Upcoming" ? isUpcoming : !isUpcoming))
      && (type === "All types" || event.type === type)
      && `${event.title} ${event.description} ${event.type}`.toLowerCase().includes(query.toLowerCase());
  }).sort((a, b) => a.date.localeCompare(b.date));
  return (
    <>
      <PageHero eyebrow="Events & activities" title="A reason to come together." description="A home for talks, workshops, technical gatherings, and student-led experiences." />
      <section className="section-pad"><div className="container"><SampleNote>Event names and dates below are sample-only and must not be treated as a real schedule.</SampleNote><SectionHeading eyebrow="What's happening" title="Find your next moment." description="Filter by timing or event type to explore the sample listings." /><div className="filter-toolbar event-filter"><label className="search-field"><Search size={18} /><input type="search" placeholder="Search events" value={query} onChange={(event) => setQuery(event.target.value)} /><span className="sr-only">Search events</span></label><label className="select-field"><span className="sr-only">Filter by event timing</span><select value={period} onChange={(event) => setPeriod(event.target.value)}><option>All events</option><option>Upcoming</option><option>Past</option></select></label><label className="select-field"><span className="sr-only">Filter by event type</span><select value={type} onChange={(event) => setType(event.target.value)}><option>All types</option>{eventTypes.map((item) => <option key={item}>{item}</option>)}</select></label></div><p className="result-count">{filtered.length} sample {filtered.length === 1 ? "event" : "events"}</p><div className="event-list">{filtered.map((event) => <EventCard key={event.id} event={event} />)}</div>{filtered.length === 0 && <EmptyState title="No events match those filters." text="Try a different search or filter." />}</div></section>
    </>
  );
}

function EventDetailPage() {
  const { id } = useParams();
  const event = events.find((item) => item.id === id);
  if (!event) return <NotFoundPage />;
  return (
    <>
      <PageHero eyebrow={`${event.type} · sample event`} title={event.title} description={event.description} />
      <section className="section-pad"><div className="container detail-layout"><div className="detail-back"><Link className="text-link" to="/events"><ArrowRight className="back-arrow" size={16} /> Back to events</Link></div><div className="detail-main"><SampleNote>This is an example event detail. The date and venue are placeholders, and registration is not open.</SampleNote><div className="detail-info-grid"><div><span>Date</span><strong>{formatDate(event.date)} · sample</strong></div><div><span>Venue</span><strong>{event.venue}</strong></div><div><span>Event type</span><strong>{event.type}</strong></div><div><span>Registration</span><strong>Verified registration details to be added</strong></div></div><h2>About this gathering</h2><p className="intro-lead">{event.description} This page can hold a confirmed schedule, speaker details, accessibility information, and registration link.</p></div></div></section>
    </>
  );
}

function AchievementsPage() {
  const categories = ["All", ...Array.from(new Set(achievements.map((item) => item.category)))];
  const [category, setCategory] = useState("All");
  const filtered = achievements.filter((item) => category === "All" || item.category === category);
  return (
    <>
      <PageHero eyebrow="Achievements" title="Small steps. Meaningful milestones." description="Celebrate verified student and faculty work, research contributions, and community impact." />
      <section className="section-pad"><div className="container"><SampleNote>Every achievement listed is a sample placeholder; no real award or individual is claimed.</SampleNote><SectionHeading eyebrow="The achievement timeline" title="Work worth sharing." description="A considered timeline that can grow with verified stories from the department." /><div className="filter-chips achievement-filters" aria-label="Filter achievements">{categories.map((item) => <button key={item} className={category === item ? "filter-chip active" : "filter-chip"} type="button" aria-pressed={category === item} onClick={() => setCategory(item)}>{item}</button>)}</div><div className="achievement-timeline">{filtered.map((item, index) => <article className="achievement-row" key={item.title}><div className="achievement-track"><span className="achievement-dot"><Award size={17} /></span><span className="achievement-line" /></div><div className="achievement-content"><span className="achievement-year">{item.year} · {item.category}</span><h3>{item.title}</h3><p>{item.detail}</p></div><span className="achievement-number">0{index + 1}</span></article>)}</div></div></section>
    </>
  );
}

function StudentLifePage() {
  return (
    <>
      <PageHero eyebrow="Student life" title="Find your people. Follow your curiosity." description="The best learning happens in community: in clubs, project teams, peer groups, and shared experiments." image="https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=1800&q=85" />
      <section className="student-life-story section-pad"><div className="container life-story-grid"><div><span className="eyebrow">Outside the lecture hall</span><h2>Make things. Make friends. Make it yours.</h2><p>Student communities make space to try ideas early, ask questions openly, and learn alongside people who care about the same things.</p><Link to="/events" className="text-link">Explore sample events <ArrowRight size={16} /></Link></div><div className="life-stat-stack"><div><strong>01</strong><span>Learn through making</span></div><div><strong>02</strong><span>Share what you discover</span></div><div><strong>03</strong><span>Build with one another</span></div></div></div></section>
      <section className="section-pad"><div className="container"><SampleNote>Club names and activities below are fictional examples. Replace with official club details and verified contact/join information.</SampleNote><SectionHeading eyebrow="Communities to explore" title="A place for every kind of curious." description="Sample club cards show how student communities can introduce their focus and activities." /><div className="club-grid">{clubs.map((club, index) => <article className="club-card" key={club.name}><span className="club-index">0{index + 1}</span><div className="club-emblem">{index === 0 ? <Code2 size={22} /> : index === 1 ? <BrainCircuit size={22} /> : <Network size={22} />}</div><span className="eyebrow">{club.focus}</span><h3>{club.name}</h3><p>{club.description}</p><ul>{club.activities.map((activity) => <li key={activity}><Check size={14} />{activity}</li>)}</ul><Link className="text-link" to="/contact">Ask about getting involved <ArrowRight size={15} /></Link></article>)}</div></div></section>
    </>
  );
}

function CareersPage() {
  const resources = [
    { icon: FileText, title: "Build a clear CV", text: "A practical guide to presenting projects, skills, and experience with clarity." },
    { icon: Code2, title: "Prepare for interviews", text: "A structured path for practising problem-solving and technical conversations." },
    { icon: BriefcaseBusiness, title: "Find an internship", text: "Verified opportunities and application resources can be shared here." },
  ];
  return (
    <>
      <PageHero eyebrow="Careers & opportunities" title="Prepare for what comes next." description="Support for career exploration, internships, technical interviews, and the many paths computing can open." />
      <section className="section-pad"><div className="container career-intro"><div><span className="eyebrow">Careers are built, not announced</span><h2>Confidence grows through practice.</h2><p>Career development starts with making things, learning from feedback, and understanding how your skills can contribute. This page can connect students to verified opportunities and resources.</p></div><div className="career-note"><BriefcaseBusiness size={23} /><span>Opportunity board</span><strong>Awaiting verified listings</strong><p>No recruiter partnerships, placement statistics, or live opportunities are claimed here.</p></div></div></section>
      <section className="career-resources section-pad" id="resources"><div className="container"><SectionHeading eyebrow="Useful starting points" title="Build your toolkit." description="Sample career resource cards can link to department-approved guidance." /><div className="resource-grid">{resources.map(({ icon: Icon, title, text }, index) => <article className="resource-card" key={title}><span className="resource-number">0{index + 1}</span><Icon size={22} /><h3>{title}</h3><p>{text}</p><Link to="/contact" className="text-link">Ask about resources <ArrowRight size={15} /></Link></article>)}</div></div></section>
      <section className="section-pad">
        <div className="container">
          <SectionHeading eyebrow="Opportunity board" title="A clear path to what’s next." description="Sample announcement types that can be populated with verified career information." />
          <div className="career-opportunity-grid">
            {[
              ["Internship announcements", "Verified opportunities and application dates will appear here."],
              ["Placement preparation", "Department-approved interview and placement resources will appear here."],
              ["Industry sessions", "Confirmed career events and industry sessions will appear here."],
              ["Alumni journeys", "Stories shared with alumni consent will appear here."],
            ].map(([title, text], index) => <article key={title}><span>0{index + 1} · SAMPLE FORMAT</span><h3>{title}</h3><p>{text}</p></article>)}
          </div>
        </div>
      </section>
      <section className="section-pad career-journey"><div className="container"><span className="eyebrow eyebrow-light">A thoughtful next step</span><h2>Bring your questions.<br /><em>Let's start a conversation.</em></h2><Link to="/contact" className="button button-light">Contact the department <ArrowRight size={16} /></Link></div></section>
    </>
  );
}

function NoticesPage() {
  const categories = ["All categories", ...Array.from(new Set(notices.map((notice) => notice.category)))];
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All categories");
  const [date, setDate] = useState("");
  const filtered = notices.filter((notice) => {
    const matchesQuery = `${notice.title} ${notice.summary} ${notice.category}`.toLowerCase().includes(query.toLowerCase());
    return matchesQuery && (category === "All categories" || notice.category === category) && (!date || notice.date === date);
  }).sort((a, b) => Number(b.important) - Number(a.important) || b.date.localeCompare(a.date));
  return (
    <>
      <PageHero eyebrow="Department notice board" title="Important things, in one place." description="A clear notice board for academic updates, events, examinations, internships, and student announcements." />
      <section className="section-pad"><div className="container"><SampleNote>All notices and dates are examples only. Check verified official department communications for current information.</SampleNote><SectionHeading eyebrow="Notice board" title="Browse department updates." description="Search by keyword, category, or sample publication date." /><div className="filter-toolbar notice-filters"><label className="search-field"><Search size={18} /><input type="search" placeholder="Search notices" value={query} onChange={(event) => setQuery(event.target.value)} /><span className="sr-only">Search notices</span></label><label className="select-field"><span className="sr-only">Filter notices by category</span><select value={category} onChange={(event) => setCategory(event.target.value)}>{categories.map((item) => <option key={item}>{item}</option>)}</select></label><label className="date-field"><CalendarDays size={16} /><span className="sr-only">Filter notices by date</span><input type="date" value={date} onChange={(event) => setDate(event.target.value)} /></label></div><p className="result-count">{filtered.length} sample {filtered.length === 1 ? "notice" : "notices"}</p><div className="notice-list">{filtered.map((notice) => <Link className={`notice-card${notice.important ? " notice-important" : ""}`} key={notice.id} to={`/notices/${notice.id}`}><div className="notice-card-meta"><span className="notice-category">{notice.category}</span>{notice.important && <span className="important-badge">Important</span>}<time dateTime={notice.date}>{formatDate(notice.date)} · sample</time></div><h3>{notice.title}</h3><p>{notice.summary}</p><span className="notice-read">Read notice <ArrowRight size={15} /></span></Link>)}</div>{filtered.length === 0 && <EmptyState title="No notices match those filters." text="Try another keyword, category, or date." />}</div></section>
    </>
  );
}

function NoticeDetailPage() {
  const { id } = useParams();
  const notice = notices.find((item) => item.id === id);
  if (!notice) return <NotFoundPage />;
  return (
    <>
      <PageHero eyebrow={`${notice.category} · sample notice`} title={notice.title} description={notice.summary} />
      <section className="section-pad"><div className="container detail-layout"><div className="detail-back"><Link className="text-link" to="/notices"><ArrowRight className="back-arrow" size={16} /> Back to notices</Link></div><div className="detail-main"><SampleNote>This notice is demonstration content, not an official announcement.</SampleNote><div className="detail-info-grid"><div><span>Category</span><strong>{notice.category}</strong></div><div><span>Published</span><strong>{formatDate(notice.date)} · sample</strong></div><div><span>Priority</span><strong>{notice.important ? "Important · sample" : "Standard · sample"}</strong></div><div><span>Attachments</span><strong>No attachments in this demo</strong></div></div><h2>Notice details</h2><p className="intro-lead">{notice.summary}</p><p>Official instructions, deadlines, and supporting attachments should be added only after the department verifies the notice.</p></div></div></section>
    </>
  );
}

function ContactPage() {
  const [formStatus, setFormStatus] = useState<"idle" | "error" | "success">("idle");
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = event.currentTarget;
    if (!form.reportValidity()) {
      setFormStatus("error");
      return;
    }
    setFormStatus("success");
    form.reset();
  };
  return (
    <>
      <PageHero eyebrow="Contact" title="Start a conversation." description="Questions about studying, research, student projects, or collaborating? We would be glad to hear from you." />
      <section className="section-pad"><div className="container contact-grid"><div className="contact-information"><span className="eyebrow">Get in touch</span><h2>We’re listening.</h2><p>Official contact details are intentionally not listed until they can be verified by the department.</p><div className="contact-detail"><span><MapPin size={18} /></span><div><strong>Department location</strong><p>Official campus directions to be confirmed.</p></div></div><div className="contact-detail"><span><Mail size={18} /></span><div><strong>Email</strong><p>Verified department email to be added.</p></div></div><div className="contact-detail"><span><Users size={18} /></span><div><strong>Faculty contact</strong><p>Verified faculty contacts to be added.</p></div></div><a className="text-link map-link" href="https://maps.google.com/?q=BMS+Institute+of+Technology+and+Management+Bengaluru" target="_blank" rel="noreferrer">Search campus location on Maps <ExternalLink size={15} /></a><SampleNote>The map link is a general search, not an official campus pin.</SampleNote></div><div className="contact-form-panel"><div className="form-heading"><span className="eyebrow">Send an enquiry</span><h2>What would you like to know?</h2><p>This demonstration form validates in your browser. It does not send or store a message.</p></div><form className="contact-form" onSubmit={handleSubmit} noValidate><div className="form-row"><label>Your name<input name="name" autoComplete="name" placeholder="Name" required /></label><label>Email address<input name="email" type="email" autoComplete="email" placeholder="you@example.com" required /></label></div><label>I'm getting in touch about<select name="topic" defaultValue="" required><option value="" disabled>Select a topic</option><option>Prospective student enquiry</option><option>Academic information</option><option>Research collaboration</option><option>Student project showcase</option><option>Other</option></select></label><label>Your message<textarea name="message" rows={5} placeholder="Tell us a little about your enquiry..." minLength={10} required /></label><button className="button button-navy" type="submit">Validate enquiry <ArrowRight size={16} /></button>{formStatus === "error" && <p className="form-message form-error" role="alert">Please complete all required fields with a valid email address and a message of at least 10 characters.</p>}{formStatus === "success" && <p className="form-message form-success" role="status"><Check size={17} /> Your details passed local validation. Nothing was sent or saved; connect a verified mailbox or backend before publishing.</p>}</form></div></div></section>
    </>
  );
}

function EmptyState({ title, text }: { title: string; text: string }) {
  return <div className="empty-state"><Search size={23} /><h3>{title}</h3><p>{text}</p></div>;
}

function NotFoundPage() {
  return <section className="not-found"><div className="container"><span className="eyebrow">404 · page not found</span><h1>This page is not here.</h1><p>The link may have changed, or the page may not exist yet.</p><Link className="button button-navy" to="/">Return to the homepage <ArrowRight size={16} /></Link></div></section>;
}

function formatDate(value: string) {
  return new Date(`${value}T12:00:00`).toLocaleDateString("en", { day: "numeric", month: "short", year: "numeric" });
}

export default function App() {
  return <SiteLayout />;
}
