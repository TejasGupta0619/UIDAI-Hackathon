import { X } from "lucide-react";

type Props = {
  open: boolean;
  onClose: () => void;
};

export default function ScreenReaderModal({ open, onClose }: Props) {
  if (!open) return null;

  return (
    <div className="modal-overlay" role="dialog" aria-modal="true">
      <div className="modal">
        <div className="modal-header">
          <h3>Screen Reader Access</h3>
          <button className="modal-close" aria-label="Close" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        <div className="modal-body">
          <p>
            The HACKATHON (UIDAI HACKATHON 2026 - TEAMBOLT) Website complies with
            World Wide Web Consortium (W3C) Web Content Accessibility Guidelines
            (WCAG) 2.0 level AA and Guidelines for Indian Government Websites.
          </p>

          <p>
            This enables people with visual impairments to access the Website
            using assistive technologies, such as screen readers. The
            information on the Website is accessible with different screen
            readers, such as JAWS, NVDA, SAFA, Supernova and Window-Eyes.
          </p>

          <p>
            <strong>Supported Screen Readers</strong>
          </p>

          <table className="sr-table">
            <thead>
              <tr>
                <th>Screen Reader</th>
                <th>Website</th>
                <th>Free / Commercial</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Non Visual Desktop Access (NVDA)</td>
                <td>
                  <a
                    href="http://www.nvda-project.org/"
                    target="_blank"
                    rel="noopener"
                  >
                    http://www.nvda-project.org/
                  </a>
                </td>
                <td>Free</td>
              </tr>

              <tr>
                <td>System Access To Go</td>
                <td>
                  <a
                    href="http://www.satogo.com/"
                    target="_blank"
                    rel="noopener"
                  >
                    http://www.satogo.com/
                  </a>
                </td>
                <td>Free</td>
              </tr>

              <tr>
                <td>Hal</td>
                <td>
                  <a
                    href="http://www.yourdolphin.co.uk/productdetail.asp?id=5"
                    target="_blank"
                    rel="noopener"
                  >
                    yourdolphin.co.uk
                  </a>
                </td>
                <td>Commercial</td>
              </tr>

              <tr>
                <td>Supernova</td>
                <td>
                  <a
                    href="http://www.yourdolphin.co.uk/productdetail.asp?id=1"
                    target="_blank"
                    rel="noopener"
                  >
                    yourdolphin.co.uk
                  </a>
                </td>
                <td>Commercial</td>
              </tr>

              <tr>
                <td>Window-Eyes</td>
                <td>
                  <a
                    href="http://www.gwmicro.com/Window-Eyes/"
                    target="_blank"
                    rel="noopener"
                  >
                    gwmicro.com
                  </a>
                </td>
                <td>Commercial</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
