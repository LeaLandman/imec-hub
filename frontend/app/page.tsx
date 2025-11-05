
"use client";
import { useEffect, useState } from "react";
import { fetchJSON } from "../lib/api";

function KPI({ label, value }: { label: string; value: string | number }) {
  return (
    <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 12, minWidth: 160 }}>
      <div style={{ fontSize: 12, opacity: 0.7 }}>{label}</div>
      <div style={{ fontSize: 22, fontWeight: 700 }}>{value}</div>
    </div>
  );
}

export default function HomePage() {
  const [items, setItems] = useState<any[]>([]);
  const [lang, setLang] = useState<string>("fr");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const l = params.get("lang") || "fr";
    setLang(l);
    fetchJSON("/search").then((d) => setItems(d.items || []));
  }, []);

  const dir = lang === "ar" ? "rtl" : "ltr";
  const t = (k: string) => {
    const m: Record<string, Record<string, string>> = {
      fr: { title: "Vue intégrée IMEC", budgets: "Budgets récents", news: "Dernières actus", legal: "Cadre légal" },
      en: { title: "Integrated IMEC view", budgets: "Recent budgets", news: "Latest news", legal: "Legal framework" },
      ar: { title: "نظرة متكاملة على IMEC", budgets: "أحدث الميزانيات", news: "آخر الأخبار", legal: "الإطار القانوني" }
    };
    return m[lang]?.[k] || k;
  };

  const budgets = items.filter((x) => x.type === "budget");
  const news = items.filter((x) => x.type === "news");
  const legal = items.filter((x) => x.type === "legal");

  return (
    <div dir={dir} style={{ display: "grid", gap: 16 }}>
      <h1>{t("title")}</h1>
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <KPI label="Items" value={items.length} />
        <KPI label="Budgets" value={budgets.length} />
        <KPI label="News" value={news.length} />
        <KPI label="Legal" value={legal.length} />
      </div>

      <section>
        <h2>{t("budgets")}</h2>
        <div style={{ display: "grid", gap: 8 }}>
          {budgets.map((b, i) => (
            <div key={i} style={{ padding: 12, border: "1px solid #eee", borderRadius: 8 }}>
              <div><strong>{b.segment?.toUpperCase()}</strong> • {b.currency} {b.amount_original}</div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>{b.date} • {b.countries_involved?.join(", ")}</div>
              <div style={{ marginTop: 4 }}>{(lang === "fr" && b.summary_fr) || (lang === "en" && b.summary_en) || (lang === "ar" && b.summary_ar)}</div>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>{t("news")}</h2>
        <div style={{ display: "grid", gap: 8 }}>
          {news.map((n, i) => (
            <div key={i} style={{ padding: 12, border: "1px solid #eee", borderRadius: 8 }}>
              <div><strong>{n.title}</strong> • {n.date}</div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>{n.outlet}</div>
              <div style={{ marginTop: 4 }}>{(lang === "fr" && n.summary_fr) || (lang === "en" && n.summary_en) || (lang === "ar" && n.summary_ar)}</div>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>{t("legal")}</h2>
        <div style={{ display: "grid", gap: 8 }}>
          {legal.map((l, i) => (
            <div key={i} style={{ padding: 12, border: "1px solid #eee", borderRadius: 8 }}>
              <div><strong>{l.instrument_type?.toUpperCase()}</strong> • {l.title}</div>
              <div style={{ fontSize: 12, opacity: 0.7 }}>{l.country_id}{l.adoption_date ? " • " + l.adoption_date : ""}{l.number ? " • " + l.number : ""}</div>
              <div style={{ marginTop: 4 }}>{(lang === "fr" && l.summary_fr) || (lang === "en" && l.summary_en) || (lang === "ar" && l.summary_ar)}</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
