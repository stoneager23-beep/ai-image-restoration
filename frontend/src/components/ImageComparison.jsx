import { useState, useRef, useEffect, useCallback } from 'react';
import './ImageComparison.css';

/**
 * Before/After image comparison slider.
 * Drag the handle to reveal original (left) vs restored (right).
 */
export default function ImageComparison({ originalUrl, restoredUrl }) {
  const [sliderPos, setSliderPos] = useState(50);
  const containerRef = useRef(null);
  const dragging = useRef(false);

  const updatePosition = useCallback((clientX) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const x = clientX - rect.left;
    const percent = Math.max(0, Math.min(100, (x / rect.width) * 100));
    setSliderPos(percent);
  }, []);

  const handlePointerDown = useCallback((e) => {
    e.preventDefault();
    dragging.current = true;
    updatePosition(e.clientX);
  }, [updatePosition]);

  useEffect(() => {
    const handlePointerMove = (e) => {
      if (!dragging.current) return;
      updatePosition(e.clientX);
    };

    const handlePointerUp = () => {
      dragging.current = false;
    };

    window.addEventListener('pointermove', handlePointerMove);
    window.addEventListener('pointerup', handlePointerUp);

    return () => {
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('pointerup', handlePointerUp);
    };
  }, [updatePosition]);

  return (
    <div className="comparison-wrapper">
      <div
        className="comparison-container"
        ref={containerRef}
        onPointerDown={handlePointerDown}
      >
        {/* Original image — full width, bottom layer */}
        <img
          src={originalUrl}
          alt="Original"
          className="comparison-img comparison-img-original"
          draggable={false}
        />

        {/* Restored image — clipped to the right of the slider */}
        <div
          className="comparison-overlay"
          style={{ clipPath: `inset(0 0 0 ${sliderPos}%)` }}
        >
          <img
            src={restoredUrl}
            alt="Restored"
            className="comparison-img comparison-img-restored"
            draggable={false}
          />
        </div>

        {/* Labels */}
        <span className="comparison-label comparison-label-left">Original</span>
        <span className="comparison-label comparison-label-right">Restored</span>

        {/* Slider line + handle */}
        <div className="comparison-slider-line" style={{ left: `${sliderPos}%` }}>
          <div className="comparison-handle">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <polyline points="8 4 4 12 8 20" />
              <polyline points="16 4 20 12 16 20" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );
}
