import { useState, useEffect } from "react";

// ─── DESIGN TOKENS ────────────────────────────────────────────────────────────
// Spacing: 8pt grid (4, 8, 12, 16, 20, 24, 32, 40, 48, 64)
// Type scale: 10 / 12 / 14 / 16 / 20 / 28 / 40 / 56
// Radii: 4 (tag) / 8 (inner) / 14 (card) / 20 (hero)
// Touch targets: 44px min / 52px primary button / 60px bottom nav

const C = {
  // 3 surface levels — no more
  base:     '#05070D',
  surface:  '#090D1C',
  card:     '#0E1424',
  elevated: '#141E30',
  // Pitch
  pitchA:   '#091C12',
  pitchB:   '#071510',
  // Borders
  hairline: 'rgba(255,255,255,0.05)',
  border:   'rgba(255,255,255,0.09)',
  // Text — all pass WCAG AA on card bg
  t1: '#EFF3FF',   // 13:1  — headlines
  t2: '#7B8FB5',   // 4.7:1 — body/secondary
  t3: '#44607C',   // labels only (large text)
  // Semantic
  amber:  '#F2C542',
  green:  '#3DC99A',
  gold:   '#FFD700',
  orange: '#F07840',
  red:    '#E85555',
  blue:   '#6090F0',
};

const MODE = {
  monitoring: { label:'MONITORING', c:C.amber,  bg:'rgba(242,197,66,0.08)',  ring:'rgba(242,197,66,0.22)', p:'pa' },
  live:       { label:'LIVE',       c:C.green,  bg:'rgba(61,201,154,0.08)', ring:'rgba(61,201,154,0.28)', p:'pg' },
  replanning: { label:'REPLANNING', c:C.orange, bg:'rgba(240,120,64,0.08)', ring:'rgba(240,120,64,0.25)', p:'po' },
};

// ─── ATOMS ────────────────────────────────────────────────────────────────────

const Tag = ({ label, color, bg, dot=true }) => (
  <span style={{
    display:'inline-flex', alignItems:'center', gap:4,
    background: bg || `${color}14`,
    border:`1px solid ${color}28`,
    color, borderRadius:4, padding:'3px 8px',
    fontFamily:'Space Mono,monospace', fontSize:9,
    fontWeight:700, letterSpacing:'0.09em', textTransform:'uppercase',
    whiteSpace:'nowrap',
  }}>
    {dot && <span style={{ width:4, height:4, borderRadius:'50%', background:color, display:'inline-block', flexShrink:0 }}/>}
    {label}
  </span>
);

const Eyebrow = ({ children }) => (
  <div style={{
    fontFamily:'Inter,sans-serif', fontSize:10, fontWeight:500,
    color:C.t3, textTransform:'uppercase', letterSpacing:'0.1em', marginBottom:12,
  }}>{children}</div>
);

const Rule = ({ my=16 }) => (
  <div style={{ height:1, background:C.hairline, margin:`${my}px 0` }} />
);

const Mono = ({ s=12, c=C.t2, children, bold }) => (
  <span style={{ fontFamily:'Space Mono,monospace', fontSize:s, color:c, fontWeight:bold?700:400, letterSpacing:'0.04em' }}>{children}</span>
);

// Primary button — 52px touch target
const BtnPrimary = ({ label, icon, onClick, color=C.amber, style:sx={} }) => (
  <button onClick={onClick} style={{
    width:'100%', height:52, borderRadius:10, border:'none', cursor:'pointer',
    background:`linear-gradient(135deg, ${color}, ${color}CC)`,
    color:'#07090D', fontFamily:'Space Grotesk,sans-serif',
    fontSize:14, fontWeight:700, letterSpacing:'0.04em',
    display:'flex', alignItems:'center', justifyContent:'center', gap:8,
    boxShadow:`0 4px 24px ${color}30`,
    transition:'opacity 0.15s, transform 0.1s',
    ...sx,
  }}
  onMouseDown={e => e.currentTarget.style.transform='scale(0.98)'}
  onMouseUp={e => e.currentTarget.style.transform='scale(1)'}
  >
    {icon && <span style={{ fontSize:17 }}>{icon}</span>}
    {label}
  </button>
);

// Ghost button — 44px touch target
const BtnGhost = ({ label, onClick, color=C.t2 }) => (
  <button onClick={onClick} style={{
    height:44, padding:'0 16px', borderRadius:8, cursor:'pointer',
    background:'transparent', border:`1px solid ${C.border}`,
    color, fontFamily:'Space Grotesk,sans-serif', fontSize:13, fontWeight:600,
    transition:'border-color 0.15s',
  }}>{label}</button>
);

// ─── PITCH CARD (hero wrapper) ────────────────────────────────────────────────
// Pitch stripes ONLY in the header area — readability safe below

const PITCH = `repeating-linear-gradient(180deg,
  rgba(9,28,18,1) 0px, rgba(9,28,18,1) 26px,
  rgba(7,21,16,1) 26px, rgba(7,21,16,1) 52px)`;

function PitchHeader({ height=160, children }) {
  return (
    <div style={{ position:'relative', height, overflow:'hidden', borderRadius:'14px 14px 0 0' }}>
      {/* grass stripes */}
      <div style={{ position:'absolute', inset:0, background:PITCH }} />
      {/* pitch lines: center spot + arc suggestions */}
      <div style={{
        position:'absolute', inset:0,
        background:`
          radial-gradient(circle 44px at 50% 50%, transparent 42px, rgba(255,255,255,0.05) 43px, rgba(255,255,255,0.05) 44px, transparent 45px),
          linear-gradient(90deg, transparent 49.5%, rgba(255,255,255,0.04) 49.8%, transparent 50.2%)
        `,
      }}/>
      {/* floodlight glows — top corners only */}
      <div style={{ position:'absolute', top:-10, left:'-5%', width:'40%', height:80, background:'radial-gradient(ellipse, rgba(242,197,66,0.14), transparent 70%)', pointerEvents:'none' }}/>
      <div style={{ position:'absolute', top:-10, right:'-5%', width:'40%', height:80, background:'radial-gradient(ellipse, rgba(242,197,66,0.14), transparent 70%)', pointerEvents:'none' }}/>
      {/* content */}
      <div style={{ position:'relative', zIndex:1, height:'100%', display:'flex', alignItems:'center', justifyContent:'center' }}>
        {children}
      </div>
    </div>
  );
}

// ─── GOAL OVERLAY ─────────────────────────────────────────────────────────────

function GoalOverlay({ visible, scorer, onDismiss }) {
  useEffect(() => {
    if (!visible) return;
    const t = setTimeout(onDismiss, 3200);
    return () => clearTimeout(t);
  }, [visible]);

  if (!visible) return null;

  return (
    <div onClick={onDismiss} style={{
      position:'fixed', inset:0, zIndex:200,
      background:'rgba(2,5,3,0.96)',
      display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center',
      cursor:'pointer',
    }}>
      <div style={{ position:'absolute', inset:0, background:PITCH, opacity:0.12 }}/>
      <div style={{
        position:'absolute', inset:0,
        background:`radial-gradient(ellipse 80% 60% at 50% 50%, rgba(255,215,0,0.08), transparent 60%)`,
      }}/>
      <div style={{ position:'relative', textAlign:'center', padding:'0 24px' }}>
        <div className="goal-ball" style={{ fontSize:52, display:'block', marginBottom:16 }}>⚽</div>
        <div className="goal-word" style={{
          fontFamily:'Space Grotesk,sans-serif', fontWeight:700,
          fontSize:'clamp(56px,16vw,80px)',
          color:C.gold, letterSpacing:'-0.04em', lineHeight:0.9,
          textShadow:`0 0 32px rgba(255,215,0,0.5), 0 0 64px rgba(255,215,0,0.2)`,
        }}>GOAAAL!</div>
        <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:16, color:C.green, fontWeight:600, marginTop:20, letterSpacing:'0.06em' }}>
          🇧🇷 {scorer}
        </div>
        <Mono s={10} c={C.t3} style={{ display:'block', marginTop:24 }}>tap to dismiss</Mono>
      </div>
    </div>
  );
}

// ─── MISSION BAR ──────────────────────────────────────────────────────────────

function MissionBar({ mission, mode = 'monitoring' }) {
  const m = MODE[mode] || MODE.monitoring;
  return (
    <div style={{
      height:56, background:C.surface,
      borderBottom:`1px solid ${C.hairline}`,
      padding:'0 20px', display:'flex',
      alignItems:'center', justifyContent:'space-between',
      position:'sticky', top:0, zIndex:50,
    }}>
      <div style={{ display:'flex', alignItems:'center', gap:12 }}>
        {/* Logo */}
        <div style={{
          width:32, height:32, borderRadius:8, flexShrink:0,
          background:`linear-gradient(135deg, #C8A000, ${C.amber})`,
          display:'flex', alignItems:'center', justifyContent:'center',
          fontSize:17, boxShadow:`0 2px 12px ${C.amber}30`,
        }}>⚽</div>
        <div>
          <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:14, fontWeight:700, color:C.t1, letterSpacing:'-0.01em', lineHeight:1.2 }}>
            {mission ? `${mission.team} · WC 2026` : 'Team · WC 2026'}
          </div>
          <div style={{ fontFamily:'Inter,sans-serif', fontSize:11, color:C.t3, marginTop:1, textTransform: 'capitalize' }}>
            {mission ? (mission.tournament_state || 'group_stage').replace('_', ' ') : 'Group Stage'}
          </div>
        </div>
      </div>
      {/* State indicator */}
      <div style={{ display:'flex', alignItems:'center', gap:7, padding:'6px 12px', background:m.bg, borderRadius:20, border:`1px solid ${m.ring}` }}>
        <span className={`p-${m.p}`} style={{ display:'inline-block', width:6, height:6, borderRadius:'50%', background:m.c, flexShrink:0 }}/>
        <Mono s={9} c={m.c} bold>{m.label}</Mono>
      </div>
    </div>
  );
}

// ─── STATUS STRIP ─────────────────────────────────────────────────────────────
// 3 key facts — scannable in < 1 second

function StatusStrip({ mode }) {
  const isLive = mode === 'live';
  const isRe   = mode === 'replanning';
  const stats  = [
    {
      icon: isRe ? '🏆' : '🇧🇷',
      label: 'Brazil',
      value: isRe ? 'Advanced' : 'Group A',
      color: isRe ? C.green : C.t1,
    },
    {
      icon: '⚽',
      label: isLive ? 'Score' : 'Kickoff',
      value: isLive ? '1 — 0' : isRe ? 'Jul 2' : '2d 14h',
      color: isLive ? C.gold : C.amber,
    },
    {
      icon: '💰',
      label: 'Budget',
      value: isRe ? '−$340' : 'On track',
      color: isRe ? C.orange : C.green,
    },
  ];

  return (
    <div style={{
      display:'flex', background:C.surface,
      borderBottom:`1px solid ${C.hairline}`,
    }}>
      {stats.map((s, i) => (
        <div key={i} style={{
          flex:1, padding:'10px 0', textAlign:'center',
          borderRight: i < 2 ? `1px solid ${C.hairline}` : 'none',
        }}>
          <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:13, fontWeight:700, color:s.color, letterSpacing:'-0.01em', lineHeight:1 }}>
            {s.value}
          </div>
          <div style={{ fontFamily:'Inter,sans-serif', fontSize:10, color:C.t3, marginTop:3 }}>{s.label}</div>
        </div>
      ))}
    </div>
  );
}

// ─── HERO: MONITORING — Next match card ──────────────────────────────────────

function HeroMonitoring() {
  return (
    <div style={{ borderRadius:14, overflow:'hidden', border:`1px solid ${C.border}` }}>
      <PitchHeader height={148}>
        <div style={{ display:'flex', alignItems:'center', width:'100%', padding:'0 20px' }}>
          {/* Team A */}
          <div style={{ flex:1, textAlign:'center' }}>
            <div style={{ fontSize:40, marginBottom:6 }}>🇧🇷</div>
            <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:13, fontWeight:700, color:'rgba(255,255,255,0.9)', letterSpacing:'0.05em', textTransform:'uppercase' }}>Brazil</div>
          </div>
          {/* Vs divider */}
          <div style={{ textAlign:'center', padding:'0 16px' }}>
            <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:24, fontWeight:700, color:'rgba(255,255,255,0.18)', letterSpacing:'0.12em' }}>VS</div>
            <Tag label="Group A" color={C.blue} dot={false}/>
          </div>
          {/* Team B */}
          <div style={{ flex:1, textAlign:'center' }}>
            <div style={{ fontSize:40, marginBottom:6 }}>🇲🇽</div>
            <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:13, fontWeight:700, color:'rgba(255,255,255,0.5)', letterSpacing:'0.05em', textTransform:'uppercase' }}>Mexico</div>
          </div>
        </div>
      </PitchHeader>

      {/* Card body — clean bg, full readability */}
      <div style={{ background:C.card, padding:20 }}>
        <div style={{ display:'flex', justifyContent:'space-between', marginBottom:16 }}>
          <div>
            <div style={{ fontFamily:'Inter,sans-serif', fontSize:11, color:C.t3, marginBottom:4 }}>Date & time</div>
            <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:15, fontWeight:600, color:C.t1 }}>Jun 22 · 19:00</div>
          </div>
          <div style={{ textAlign:'right' }}>
            <div style={{ fontFamily:'Inter,sans-serif', fontSize:11, color:C.t3, marginBottom:4 }}>Venue</div>
            <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:15, fontWeight:600, color:C.t1 }}>AT&T Stadium</div>
          </div>
        </div>

        {/* Countdown — the one big thing here */}
        <div style={{
          background:C.elevated, borderRadius:10, padding:'14px 20px',
          display:'flex', alignItems:'center', justifyContent:'space-between',
          border:`1px solid ${C.amber}22`,
        }}>
          <span style={{ fontFamily:'Inter,sans-serif', fontSize:13, color:C.t2 }}>Kickoff in</span>
          <Mono s={22} c={C.amber} bold>2d 14h 22m</Mono>
        </div>
      </div>
    </div>
  );
}

// ─── HERO: LIVE — Scoreboard ──────────────────────────────────────────────────

function HeroLive({ onGoal }) {
  return (
    <div style={{
      borderRadius:14, overflow:'hidden',
      border:`1px solid rgba(61,201,154,0.28)`,
      boxShadow:`0 0 40px rgba(61,201,154,0.06)`,
    }}>
      {/* Pitch header with live score as the dominant element */}
      <PitchHeader height={180}>
        <div style={{ width:'100%', padding:'0 20px', textAlign:'center' }}>
          {/* Live bar */}
          <div style={{ display:'flex', alignItems:'center', justifyContent:'center', gap:6, marginBottom:12 }}>
            <span className="p-pg" style={{ display:'inline-block', width:7, height:7, borderRadius:'50%', background:C.green }}/>
            <Mono s={10} c={C.green} bold>LIVE · AT&T STADIUM · 67'</Mono>
          </div>
          {/* Score — the hero element */}
          <div style={{ display:'flex', alignItems:'center', justifyContent:'center', gap:12 }}>
            <div style={{ textAlign:'center' }}>
              <div style={{ fontSize:36, marginBottom:2 }}>🇧🇷</div>
              <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:11, fontWeight:700, color:'rgba(255,255,255,0.7)', letterSpacing:'0.08em', textTransform:'uppercase' }}>Brazil</div>
            </div>
            <div style={{ textAlign:'center', padding:'0 8px' }}>
              <div style={{
                fontFamily:'Space Mono,monospace', fontWeight:700, fontSize:52,
                color:C.t1, letterSpacing:'-0.06em', lineHeight:1,
                textShadow:'0 2px 20px rgba(255,255,255,0.08)',
              }}>1—0</div>
            </div>
            <div style={{ textAlign:'center' }}>
              <div style={{ fontSize:36, marginBottom:2 }}>🇲🇽</div>
              <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:11, fontWeight:700, color:'rgba(255,255,255,0.4)', letterSpacing:'0.08em', textTransform:'uppercase' }}>Mexico</div>
            </div>
          </div>
        </div>
      </PitchHeader>

      {/* Body */}
      <div style={{ background:C.card, padding:20 }}>
        {/* Goal event */}
        <div style={{
          display:'flex', alignItems:'center', gap:10, padding:'10px 14px',
          background:`${C.gold}0C`, border:`1px solid ${C.gold}25`,
          borderRadius:8, marginBottom:16,
        }}>
          <span style={{ fontSize:16 }}>⚽</span>
          <div style={{ flex:1 }}>
            <span style={{ fontFamily:'Inter,sans-serif', fontSize:13, color:C.t1, fontWeight:500 }}>Vinicius Jr. </span>
            <Mono s={11} c={C.t3}>34'</Mono>
          </div>
          <Tag label="Goal" color={C.gold} dot={false}/>
        </div>

        {/* Win probability */}
        <div style={{ marginBottom:20 }}>
          <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:8 }}>
            <span style={{ fontFamily:'Inter,sans-serif', fontSize:13, color:C.t2 }}>Brazil win probability</span>
            <Mono s={14} c={C.green} bold>78%</Mono>
          </div>
          <div style={{ height:6, background:C.elevated, borderRadius:3, overflow:'hidden' }}>
            <div style={{ height:'100%', width:'78%', background:`linear-gradient(90deg, ${C.green}, #48BB78)`, borderRadius:3 }}/>
          </div>
        </div>

        <BtnPrimary label="Simulate Goal" icon="⚽" onClick={onGoal} color={C.gold}/>
      </div>
    </div>
  );
}

// ─── HERO: REPLANNING — Action banner ────────────────────────────────────────

function HeroReplanning({ team, onReplan, loading }) {
  return (
    <div style={{
      borderRadius:14, overflow:'hidden',
      border:`1px solid rgba(240,120,64,0.32)`,
      boxShadow:`0 0 32px rgba(240,120,64,0.07)`,
    }}>
      <PitchHeader height={100}>
        <div style={{ textAlign:'center', padding:'0 24px' }}>
          <div style={{ display:'flex', alignItems:'center', justifyContent:'center', gap:8, marginBottom:6 }}>
            <span className="p-po" style={{ display:'inline-block', width:8, height:8, borderRadius:'50%', background:C.orange }}/>
            <Mono s={10} c={C.orange} bold>ROUTE UPDATE REQUIRED</Mono>
          </div>
          <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:22, fontWeight:700, color:C.t1, letterSpacing:'-0.02em', lineHeight:1.2 }}>
            {team || 'Team'} advanced 🏆
          </div>
        </div>
      </PitchHeader>
      <div style={{ background:C.card, padding:20 }}>
        <p style={{ fontFamily:'Inter,sans-serif', fontSize:14, color:C.t2, lineHeight:1.6, margin:'0 0 16px' }}>
          {team || 'The team'} qualified as <strong style={{ color:C.t1 }}>Group A winners</strong>. Round of 16 moves to <strong style={{ color:C.t1 }}>Seattle on Jul 2</strong>. Chicago is no longer on your route.
        </p>
        <div style={{ display:'flex', gap:8 }}>
          <BtnPrimary 
            label={loading ? 'Generating...' : 'Generate Recommendation'} 
            onClick={onReplan} 
            color={C.orange} 
            style={{ flex:1, width:'auto', opacity: loading ? 0.7 : 1 }}
          />
          <BtnGhost label="Later" color={C.t3}/>
        </div>
      </div>
    </div>
  );
}

// ─── JOURNEY TIMELINE ─────────────────────────────────────────────────────────
// Visual route with clear progression — not a list

function JourneyTimeline({ mode }) {
  const isRe = mode === 'replanning';
  const stops = isRe
    ? [
        { city:'Los Angeles', flag:'🏟', match:'Match 1', status:'done' },
        { city:'Seattle', flag:'🏟', match:'Round of 16', status:'next', changed:true },
        { city:'TBD', flag:'⬡', match:'Quarter Final', status:'projected' },
      ]
    : [
        { city:'Los Angeles', flag:'🏟', match:'Match 1', status:'done' },
        { city:'Dallas', flag:'🏟', match:'Match 2', status: mode==='live' ? 'active' : 'next' },
        { city:'New York', flag:'🏟', match:'Match 3', status:'future' },
      ];

  const sc = { done:C.t3, active:C.green, next:C.amber, future:C.t3, projected:'#4A6080' };
  const nodeBg = { done:C.elevated, active:`${C.green}1A`, next:`${C.amber}14`, future:C.elevated, projected:`${C.blue}10` };
  const nodeBorder = { done:C.border, active:`${C.green}40`, next:`${C.amber}40`, future:C.hairline, projected:`${C.blue}30` };

  return (
    <div style={{ background:C.card, borderRadius:14, border:`1px solid ${C.border}`, padding:20 }}>
      <Eyebrow>Your journey</Eyebrow>
      <div style={{ position:'relative' }}>
        {/* Connecting line */}
        <div style={{
          position:'absolute', left:19, top:24, bottom:24,
          width:2, background:C.hairline, zIndex:0,
        }}/>
        <div style={{ display:'flex', flexDirection:'column', gap:0 }}>
          {stops.map((stop, i) => {
            const isActive = stop.status === 'active' || stop.status === 'next';
            return (
              <div key={i} style={{
                display:'flex', alignItems:'center', gap:14,
                padding:'10px 0', position:'relative', zIndex:1,
                minHeight:44, // touch target consideration
              }}>
                {/* Node */}
                <div style={{
                  width:40, height:40, borderRadius:10, flexShrink:0,
                  background:nodeBg[stop.status],
                  border:`1.5px solid ${nodeBorder[stop.status]}`,
                  display:'flex', alignItems:'center', justifyContent:'center',
                  fontSize: stop.status === 'done' ? 14 : 18,
                }}>
                  {stop.flag}
                </div>
                {/* Details */}
                <div style={{ flex:1 }}>
                  <div style={{ fontFamily:'Space Grotesk,sans-serif', fontSize:14, fontWeight:700, color:isActive ? C.t1 : C.t2, letterSpacing:'-0.01em' }}>
                    {stop.city}
                  </div>
                  <div style={{ fontFamily:'Inter,sans-serif', fontSize:12, color:C.t3, marginTop:2 }}>
                    {stop.match}
                  </div>
                </div>
                {/* Right side tag */}
                {stop.changed && <Tag label="UPDATED" color={C.orange} dot={false}/>}
                {stop.status === 'done' && <Mono s={14} c={C.green}>✓</Mono>}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export {
  Tag, Eyebrow, Rule, Mono, BtnPrimary, BtnGhost,
  PitchHeader, GoalOverlay, MissionBar, StatusStrip,
  HeroMonitoring, HeroLive, HeroReplanning, JourneyTimeline
};