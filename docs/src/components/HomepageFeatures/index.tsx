import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Get / Build VyOS',
    Svg: require('@site/static/img/vyos_logo.svg').default,
    description: (
      <>
        Quickly Build your own Image or take a look at how to download a
        free or supported version.
      </>
    ),
  },
  {
    title: 'Install VyOS',
    Svg: require('@site/static/img/vyos_logo.svg').default,
    description: (
      <>
        Read about how to install VyOS on Bare Metal or in a Virtual Environment
        and how to use an image with the usual cloud providers
      </>
    ),
  },
  {
    title: 'Configuration and Operation',
    Svg: require('@site/static/img/vyos_logo.svg').default,
    description: (
      <>
        Use the Quickstart Guide, to have a fast overview.
        Or go deeper and set up advanced routing, VRFs, or VPNs for example.
      </>
    ),
  },
  {
    title: 'Automate',
    Svg: require('@site/static/img/vyos_logo.svg').default,
    description: (
      <>
        Integrate VyOS in your automation Workflow with Ansible,
        have your own local scripts, or configure VyOS with the HTTPS-API.
      </>
    ),
  },
  {
    title: 'Examples',
    Svg: require('@site/static/img/vyos_logo.svg').default,
    description: (
      <>
        Get some inspiration from the Configuration Blueprints
        to build your infrastructure.
      </>
    ),
  },
  {
    title: 'Contribute and Community',
    Svg: require('@site/static/img/vyos_logo.svg').default,
    description: (
      <>        
        There are many ways to contribute to the project.
        Add missing parts or improve the Documentation.
        Discuss in Slack or the Forum.
        Or you can pick up a Task and fix the code.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
