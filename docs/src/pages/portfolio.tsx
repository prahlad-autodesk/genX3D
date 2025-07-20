import React from 'react';
import type {JSX} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './portfolio.module.css';

export default function Portfolio(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title="Portfolio"
      description="Showcase of genx3D projects and capabilities">
      <main className={styles.main}>
        <div className={styles.hero}>
          <div className={styles.heroContent}>
            <h1 className={styles.heroTitle}>
              genx3D Portfolio
            </h1>
            <p className={styles.heroSubtitle}>
              Showcasing innovative 3D CAD projects powered by AI
            </p>
          </div>
        </div>

        <div className={styles.container}>
          {/* Featured Projects */}
          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Featured Projects</h2>
            <div className={styles.projectGrid}>
              <div className={styles.projectCard}>
                <div className={styles.projectImage}>
                  <img src="/img/portfolio/gear-system.png" alt="Gear System" />
                </div>
                <div className={styles.projectContent}>
                  <h3>Parametric Gear System</h3>
                  <p>Complex gear assembly with 20+ interlocking components, generated using AI-assisted design.</p>
                  <div className={styles.projectTags}>
                    <span className={styles.tag}>Parametric</span>
                    <span className={styles.tag}>Assembly</span>
                    <span className={styles.tag}>AI-Generated</span>
                  </div>
                  <Link to="/docs/tutorials/first-model" className={styles.projectLink}>
                    View Tutorial →
                  </Link>
                </div>
              </div>

              <div className={styles.projectCard}>
                <div className={styles.projectImage}>
                  <img src="/img/portfolio/architectural-model.png" alt="Architectural Model" />
                </div>
                <div className={styles.projectContent}>
                  <h3>Architectural Pavilion</h3>
                  <p>Modern architectural design featuring complex geometric patterns and organic forms.</p>
                  <div className={styles.projectTags}>
                    <span className={styles.tag}>Architecture</span>
                    <span className={styles.tag}>Organic</span>
                    <span className={styles.tag}>Complex Geometry</span>
                  </div>
                  <Link to="/docs/tutorials/customization" className={styles.projectLink}>
                    Learn More →
                  </Link>
                </div>
              </div>

              <div className={styles.projectCard}>
                <div className={styles.projectImage}>
                  <img src="/img/portfolio/mechanical-part.png" alt="Mechanical Part" />
                </div>
                <div className={styles.projectContent}>
                  <h3>Precision Mechanical Part</h3>
                  <p>High-precision component with tight tolerances and complex internal features.</p>
                  <div className={styles.projectTags}>
                    <span className={styles.tag}>Precision</span>
                    <span className={styles.tag}>Manufacturing</span>
                    <span className={styles.tag}>Analysis</span>
                  </div>
                  <Link to="/docs/features/model-analysis" className={styles.projectLink}>
                    View Analysis →
                  </Link>
                </div>
              </div>
            </div>
          </section>

          {/* Capabilities */}
          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Platform Capabilities</h2>
            <div className={styles.capabilitiesGrid}>
              <div className={styles.capabilityCard}>
                <div className={styles.capabilityIcon}>🎨</div>
                <h3>3D CAD Modeling</h3>
                <p>Browser-based parametric modeling with real-time visualization and manipulation.</p>
                <ul>
                  <li>Parametric design</li>
                  <li>Real-time rendering</li>
                  <li>STEP/STL export</li>
                </ul>
              </div>

              <div className={styles.capabilityCard}>
                <div className={styles.capabilityIcon}>🤖</div>
                <h3>AI Assistant</h3>
                <p>Intelligent chat interface for CAD assistance and model generation.</p>
                <ul>
                  <li>Natural language input</li>
                  <li>Code generation</li>
                  <li>Design suggestions</li>
                </ul>
              </div>

              <div className={styles.capabilityCard}>
                <div className={styles.capabilityIcon}>⚡</div>
                <h3>High Performance</h3>
                <p>FastAPI backend with LangGraph orchestration for complex workflows.</p>
                <ul>
                  <li>Rapid API responses</li>
                  <li>Workflow orchestration</li>
                  <li>Scalable architecture</li>
                </ul>
              </div>

              <div className={styles.capabilityCard}>
                <div className={styles.capabilityIcon}>🔧</div>
                <h3>Developer Friendly</h3>
                <p>Comprehensive API and documentation for easy integration.</p>
                <ul>
                  <li>RESTful APIs</li>
                  <li>Open source</li>
                  <li>Extensible architecture</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Use Cases */}
          <section className={styles.section}>
            <h2 className={styles.sectionTitle}>Use Cases</h2>
            <div className={styles.useCasesGrid}>
              <div className={styles.useCaseCard}>
                <h3>Education</h3>
                <p>Teach 3D modeling and CAD principles with an intuitive web-based interface.</p>
                <Link to="/docs/tutorials/first-model" className={styles.useCaseLink}>
                  Educational Tutorials →
                </Link>
              </div>

              <div className={styles.useCaseCard}>
                <h3>Prototyping</h3>
                <p>Rapidly prototype mechanical designs with AI-assisted modeling.</p>
                <Link to="/docs/features/model-generation" className={styles.useCaseLink}>
                  Prototyping Guide →
                </Link>
              </div>

              <div className={styles.useCaseCard}>
                <h3>Manufacturing</h3>
                <p>Generate production-ready models with precise tolerances and analysis.</p>
                <Link to="/docs/features/model-analysis" className={styles.useCaseLink}>
                  Manufacturing Guide →
                </Link>
              </div>

              <div className={styles.useCaseCard}>
                <h3>Research</h3>
                <p>Explore complex geometries and parametric relationships for research projects.</p>
                <Link to="/docs/features/3d-cad-modeling" className={styles.useCaseLink}>
                  Research Applications →
                </Link>
              </div>
            </div>
          </section>

          {/* Call to Action */}
          <section className={styles.ctaSection}>
            <div className={styles.ctaContent}>
              <h2>Ready to Start Creating?</h2>
              <p>Join the next generation of 3D CAD modeling with AI assistance.</p>
              <div className={styles.ctaButtons}>
                <Link to="/docs/getting-started/quick-start" className={styles.ctaButton}>
                  Get Started
                </Link>
                <Link to="/docs/api/endpoints" className={styles.ctaButtonSecondary}>
                  View API Docs
                </Link>
              </div>
            </div>
          </section>
        </div>
      </main>
    </Layout>
  );
} 