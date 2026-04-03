export default function FilterCostMobileApp() {
  const React = window.React;
  const { useMemo, useState } = React;

  const [productGroup, setProductGroup] = useState("INDUSTRIAL");
  const [filterType, setFilterType] = useState("MINI");
  const [mediaType, setMediaType] = useState("SYNTHETIC");

  const [industrial, setIndustrial] = useState({
    width: "594",
    height: "594",
    depth: "75",
    pleatCount: "100",
    packDepth: "30",
    packHeight: "594",
    frameCost: "0",
    boxCost: "2000",
    vinylCost: "500",
    sub1Name: "탈취",
    sub1Cost: "",
    sub2Name: "가스켓",
    sub2Cost: "",
    sub3Name: "인쇄부직포",
    sub3Cost: "",
    sub4Name: "비닐",
    sub4Cost: "",
    sub5Name: "에어스루",
    sub5Cost: "",
    sub6Name: "박스",
    sub6Cost: "",
    lossRate: "5",
    laborRate: "30",
    sgnaRate: "15",
    interestRate: "9",
    marginRate: "20",
    syntheticUnitCost: "12000",
    glassUnitCost: "8500",
    urethaneUnitCost: "3700",
    hotmeltUnitCost: "3900",
    foilUnitCost: "8500",
  });

  const [flat, setFlat] = useState({
    width: "300",
    height: "300",
    depth: "20",
    pleatCount: "50",
    mediaUnitCost: "12000",
    hotmeltUnitCost: "3900",
    bandUnitCost: "500",
    bandWidthMm: "20",
    frameCost: "0",
    lossRate: "5",
    laborRate: "30",
    sgnaRate: "15",
    interestRate: "9",
    marginRate: "20",
    deodorantCost: "0",
    gasketCost: "0",
    printNonwovenCost: "0",
    vinylCost: "0",
    airThroughCost: "0",
    boxCost: "0",
  });

  const [cyl, setCyl] = useState({
    width: "300",
    height: "300",
    depth: "20",
    pleatCount: "50",
    mediaUnitCost: "12000",
    hotmeltUnitCost: "3900",
    lossRate: "5",
    laborRate: "30",
    sgnaRate: "15",
    interestRate: "9",
    marginRate: "20",
    gasketCost: "0",
    honeycombCost: "0",
    carbonNonwovenCost: "0",
    meshCost: "0",
    capCost: "0",
    airThroughCost: "0",
    vinylCost: "0",
    boxCost: "0",
  });

  const num = (v, d = 0) => {
    const s = String(v ?? "").trim();
    if (!s) return d;
    const n = Number(s.replace(/,/g, ""));
    return Number.isFinite(n) ? n : d;
  };

  const setIndustrialField = (key, value) => setIndustrial((prev) => ({ ...prev, [key]: value }));
  const setFlatField = (key, value) => setFlat((prev) => ({ ...prev, [key]: value }));
  const setCylField = (key, value) => setCyl((prev) => ({ ...prev, [key]: value }));

  const industrialResults = useMemo(() => {
    const width = num(industrial.width);
    const height = num(industrial.height);
    const depth = num(industrial.depth);
    const pleatCount = num(industrial.pleatCount);
    const packDepth = num(industrial.packDepth);
    const packHeight = num(industrial.packHeight);
    const frameCost = num(industrial.frameCost);
    const boxCost = num(industrial.boxCost);
    const vinylCost = num(industrial.vinylCost);
    const sub1Cost = num(industrial.sub1Cost);
    const sub2Cost = num(industrial.sub2Cost);
    const sub3Cost = num(industrial.sub3Cost);
    const sub4Cost = num(industrial.sub4Cost);
    const sub5Cost = num(industrial.sub5Cost);
    const sub6Cost = num(industrial.sub6Cost);
    const lossRate = num(industrial.lossRate);
    const laborRate = num(industrial.laborRate);
    const sgnaRate = num(industrial.sgnaRate);
    const interestRate = num(industrial.interestRate);
    const marginRate = num(industrial.marginRate);
    const syntheticUnitCost = num(industrial.syntheticUnitCost);
    const glassUnitCost = num(industrial.glassUnitCost);
    const urethaneUnitCost = num(industrial.urethaneUnitCost);
    const hotmeltUnitCost = num(industrial.hotmeltUnitCost);
    const foilUnitCost = num(industrial.foilUnitCost);

    const mediaArea = (pleatCount * 2 * packDepth * packHeight) / 1_000_000;
    let mediaWeight = 0;
    let mediaCost = 0;
    let mediaFormula = "";

    if (mediaType === "SYNTHETIC") {
      mediaCost = mediaArea * syntheticUnitCost;
      mediaFormula = "SYNTHETIC: 면적 × 신세틱 단가(원/㎡)";
    } else {
      mediaWeight = mediaArea * 0.08;
      mediaCost = mediaWeight * glassUnitCost;
      mediaFormula = "GLASS: 면적 × 0.08kg/㎡ × 글라스 단가(원/kg)";
    }

    let foilWeight = 0;
    let foilCost = 0;
    let separatorError = "";
    if (filterType === "SEPARATOR") {
      let unitWeight = 0;
      if (depth === 292) unitWeight = 0.0198;
      else if (depth === 150) unitWeight = 0.01;
      else separatorError = "SEPARATOR TYPE은 두께 150 또는 292만 지원합니다.";
      foilWeight = pleatCount * 2 * unitWeight;
      foilCost = foilWeight * foilUnitCost;
    }

    const urethaneArea = (width * depth * 2) / 1_000_000;
    const urethaneWeight = urethaneArea * 12;
    const urethaneCost = urethaneWeight * urethaneUnitCost;

    let hotmeltLines = 0;
    let hotmeltLengthM = 0;
    let hotmeltWeightG = 0;
    let hotmeltCost = 0;
    if (filterType === "MINI") {
      hotmeltLines = height > 0 ? Math.ceil(height / 25) : 0;
      const hotmeltLengthMm = hotmeltLines * pleatCount * depth;
      hotmeltLengthM = hotmeltLengthMm / 1000;
      hotmeltWeightG = hotmeltLengthM * 2;
      hotmeltCost = (hotmeltWeightG / 1000) * hotmeltUnitCost;
    }

    const subTotal = sub1Cost + sub2Cost + sub3Cost + sub4Cost + sub5Cost + sub6Cost;
    const materialCost = mediaCost + foilCost + urethaneCost + hotmeltCost + frameCost + boxCost + vinylCost + subTotal;
    const lossCost = materialCost * (lossRate / 100);
    const subtotalAfterLoss = materialCost + lossCost;
    const laborCost = subtotalAfterLoss * (laborRate / 100);
    const sgnaCost = subtotalAfterLoss * (sgnaRate / 100);
    const interestCost = subtotalAfterLoss * (interestRate / 100);
    const totalCost = subtotalAfterLoss + laborCost + sgnaCost + interestCost;
    const sellingPrice = totalCost * (1 + marginRate / 100);

    return { separatorError, mediaArea, mediaWeight, mediaCost, mediaFormula, foilWeight, foilCost, urethaneArea, urethaneWeight, urethaneCost, hotmeltLines, hotmeltLengthM, hotmeltWeightG, hotmeltCost, frameCost, subTotal, materialCost, lossCost, laborCost, sgnaCost, interestCost, totalCost, sellingPrice };
  }, [industrial, filterType, mediaType]);

  const flatResults = useMemo(() => {
    const width = num(flat.width);
    const height = num(flat.height);
    const depth = num(flat.depth);
    const pleatCount = num(flat.pleatCount);
    const mediaUnitCost = num(flat.mediaUnitCost);
    const hotmeltUnitCost = num(flat.hotmeltUnitCost);
    const bandUnitCost = num(flat.bandUnitCost);
    const bandWidthMm = num(flat.bandWidthMm);
    const frameCost = num(flat.frameCost);
    const lossRate = num(flat.lossRate);
    const laborRate = num(flat.laborRate);
    const sgnaRate = num(flat.sgnaRate);
    const interestRate = num(flat.interestRate);
    const marginRate = num(flat.marginRate);
    const others = num(flat.deodorantCost)+num(flat.gasketCost)+num(flat.printNonwovenCost)+num(flat.vinylCost)+num(flat.airThroughCost)+num(flat.boxCost);

    const packWidth = Math.max(width - 2, 0);
    const packHeight = Math.max(height - 2, 0);
    const packDepth = Math.max(depth - 2, 0);

    const mediaArea = (pleatCount * 2 * packHeight * packDepth) / 1_000_000;
    const mediaCost = mediaArea * mediaUnitCost;

    const hotmeltLines = packHeight > 0 ? Math.ceil(packHeight / 25.4) : 0;
    const hotmeltLengthMm = hotmeltLines * pleatCount * packDepth;
    const hotmeltLengthM = hotmeltLengthMm / 1000;
    const hotmeltWeightG = hotmeltLengthM * 2;
    const hotmeltCost = (hotmeltWeightG / 1000) * hotmeltUnitCost;

    const bandLengthMm = 2 * (packWidth + packHeight);
    const bandLengthM = bandLengthMm / 1000;
    const bandCost = bandLengthM * bandUnitCost;

    const bandHotmeltArea = bandLengthM * (bandWidthMm / 1000);
    const bandHotmeltWeightKg = bandHotmeltArea * 2;
    const bandHotmeltCost = bandHotmeltWeightKg * hotmeltUnitCost;

    const materialCost = mediaCost + hotmeltCost + bandCost + bandHotmeltCost + frameCost + others;
    const lossCost = materialCost * (lossRate / 100);
    const subtotalAfterLoss = materialCost + lossCost;
    const laborCost = subtotalAfterLoss * (laborRate / 100);
    const sgnaCost = subtotalAfterLoss * (sgnaRate / 100);
    const interestCost = subtotalAfterLoss * (interestRate / 100);
    const totalCost = subtotalAfterLoss + laborCost + sgnaCost + interestCost;
    const sellingPrice = totalCost * (1 + marginRate / 100);

    return { packWidth, packHeight, packDepth, mediaArea, mediaCost, hotmeltLines, hotmeltLengthM, hotmeltWeightG, hotmeltCost, bandLengthM, bandCost, bandHotmeltWeightKg, bandHotmeltCost, others, materialCost, lossCost, laborCost, sgnaCost, interestCost, totalCost, sellingPrice };
  }, [flat]);

  const cylResults = useMemo(() => {
    const width = num(cyl.width);
    const height = num(cyl.height);
    const depth = num(cyl.depth);
    const pleatCount = num(cyl.pleatCount);
    const mediaUnitCost = num(cyl.mediaUnitCost);
    const hotmeltUnitCost = num(cyl.hotmeltUnitCost);
    const lossRate = num(cyl.lossRate);
    const laborRate = num(cyl.laborRate);
    const sgnaRate = num(cyl.sgnaRate);
    const interestRate = num(cyl.interestRate);
    const marginRate = num(cyl.marginRate);

    const mediaArea = (pleatCount * 2 * height * depth) / 1_000_000;
    const mediaCost = mediaArea * mediaUnitCost;

    const hotmeltLines = height > 0 ? Math.ceil(height / 25) : 0;
    const hotmeltLengthMm = hotmeltLines * pleatCount * depth;
    const hotmeltLengthM = hotmeltLengthMm / 1000;
    const hotmeltWeightG = hotmeltLengthM * 2;
    const hotmeltCost = (hotmeltWeightG / 1000) * hotmeltUnitCost;

    const others = num(cyl.gasketCost)+num(cyl.honeycombCost)+num(cyl.carbonNonwovenCost)+num(cyl.meshCost)+num(cyl.capCost)+num(cyl.airThroughCost)+num(cyl.vinylCost)+num(cyl.boxCost);

    const materialCost = mediaCost + hotmeltCost + others;
    const lossCost = materialCost * (lossRate / 100);
    const subtotalAfterLoss = materialCost + lossCost;
    const laborCost = subtotalAfterLoss * (laborRate / 100);
    const sgnaCost = subtotalAfterLoss * (sgnaRate / 100);
    const interestCost = subtotalAfterLoss * (interestRate / 100);
    const totalCost = subtotalAfterLoss + laborCost + sgnaCost + interestCost;
    const sellingPrice = totalCost * (1 + marginRate / 100);

    return { mediaArea, mediaCost, hotmeltLines, hotmeltLengthM, hotmeltWeightG, hotmeltCost, others, materialCost, lossCost, laborCost, sgnaCost, interestCost, totalCost, sellingPrice };
  }, [cyl]);

  const money = (n) => `${Math.round(n).toLocaleString()} 원`;
  const fixed = (n, d = 2) => Number(n).toFixed(d);

  const Field = ({ label, value, onChange, placeholder = "", type = "number" }) => (
    <label className="block">
      <div className="mb-1 text-sm font-medium text-slate-700">{label}</div>
      <input
        type={type}
        inputMode={type === "text" ? "text" : "decimal"}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full rounded-2xl border border-slate-300 bg-white px-4 py-3 text-base shadow-sm outline-none transition focus:border-slate-500"
      />
    </label>
  );

  const SegButton = ({ active, children, onClick }) => (
    <button
      onClick={onClick}
      className={`flex-1 rounded-2xl px-4 py-3 text-sm font-semibold transition ${
        active ? "bg-slate-900 text-white shadow" : "bg-white text-slate-700 border border-slate-200"
      }`}
    >
      {children}
    </button>
  );

  const Card = ({ title, children }) => (
    <section className="rounded-3xl bg-white p-4 shadow-sm border border-slate-200">
      <h2 className="mb-4 text-base font-bold text-slate-900">{title}</h2>
      <div className="space-y-3">{children}</div>
    </section>
  );

  const Row = ({ label, value, strong = false }) => (
    <div className="flex items-start justify-between gap-4 py-1">
      <div className={`text-sm ${strong ? "font-semibold text-slate-900" : "text-slate-600"}`}>{label}</div>
      <div className={`text-right text-sm ${strong ? "font-bold text-slate-900" : "text-slate-800"}`}>{value}</div>
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="mx-auto max-w-md space-y-4 p-4 pb-10">
        <div className="rounded-3xl bg-slate-900 p-5 text-white shadow-lg">
          <div className="text-xl font-bold">필터 원가 계산기</div>
          <div className="mt-1 text-sm text-slate-300">제품군별로 화면과 계산식이 바뀌는 버전</div>
        </div>

        <Card title="제품군 선택">
          <div className="flex gap-2">
            <SegButton active={productGroup === "INDUSTRIAL"} onClick={() => setProductGroup("INDUSTRIAL")}>산업용</SegButton>
            <SegButton active={productGroup === "HOME_FLAT"} onClick={() => setProductGroup("HOME_FLAT")}>가정용 평판</SegButton>
            <SegButton active={productGroup === "HOME_CYL"} onClick={() => setProductGroup("HOME_CYL")}>가정용 원형</SegButton>
          </div>
        </Card>

        {productGroup === "INDUSTRIAL" && (
          <>
            <Card title="필터 타입 선택">
              <div className="flex gap-2">
                <SegButton active={filterType === "MINI"} onClick={() => setFilterType("MINI")}>MINI TYPE</SegButton>
                <SegButton active={filterType === "SEPARATOR"} onClick={() => setFilterType("SEPARATOR")}>SEPARATOR TYPE</SegButton>
              </div>
            </Card>

            <Card title="여재 종류 선택">
              <div className="flex gap-2">
                <SegButton active={mediaType === "SYNTHETIC"} onClick={() => setMediaType("SYNTHETIC")}>SYNTHETIC</SegButton>
                <SegButton active={mediaType === "GLASS"} onClick={() => setMediaType("GLASS")}>GLASS</SegButton>
              </div>
            </Card>

            <Card title="원재료 원가설정">
              {mediaType === "SYNTHETIC" ? (
                <Field label="신세틱 원단 단가 (원/㎡)" value={industrial.syntheticUnitCost} onChange={(v) => setIndustrialField("syntheticUnitCost", v)} />
              ) : (
                <Field label="글라스 원단 단가 (원/kg)" value={industrial.glassUnitCost} onChange={(v) => setIndustrialField("glassUnitCost", v)} />
              )}
              <Field label="우레탄 단가 (원/kg)" value={industrial.urethaneUnitCost} onChange={(v) => setIndustrialField("urethaneUnitCost", v)} />
              {filterType === "MINI" && <Field label="핫멜트 단가 (원/kg)" value={industrial.hotmeltUnitCost} onChange={(v) => setIndustrialField("hotmeltUnitCost", v)} />}
              {filterType === "SEPARATOR" && <Field label="호일 단가 (원/kg)" value={industrial.foilUnitCost} onChange={(v) => setIndustrialField("foilUnitCost", v)} />}
            </Card>

            <Card title="기본 입력">
              <Field label="가로(mm)" value={industrial.width} onChange={(v) => setIndustrialField("width", v)} />
              <Field label="세로(mm)" value={industrial.height} onChange={(v) => setIndustrialField("height", v)} />
              <Field label="두께(mm)" value={industrial.depth} onChange={(v) => setIndustrialField("depth", v)} />
              <Field label="산수" value={industrial.pleatCount} onChange={(v) => setIndustrialField("pleatCount", v)} />
              <Field label="팩두께(mm)" value={industrial.packDepth} onChange={(v) => setIndustrialField("packDepth", v)} />
              <Field label="팩높이(mm)" value={industrial.packHeight} onChange={(v) => setIndustrialField("packHeight", v)} />
              <Field label="프레임 단가(원)" value={industrial.frameCost} onChange={(v) => setIndustrialField("frameCost", v)} />
              <Field label="박스 비용(원)" value={industrial.boxCost} onChange={(v) => setIndustrialField("boxCost", v)} />
              <Field label="비닐 비용(원)" value={industrial.vinylCost} onChange={(v) => setIndustrialField("vinylCost", v)} />
            </Card>

            <Card title="부자재 입력">
              <div className="grid grid-cols-2 gap-3">
                <Field label="부자재1 이름" type="text" value={industrial.sub1Name} onChange={(v) => setIndustrialField("sub1Name", v)} />
                <Field label="부자재1 금액(원)" value={industrial.sub1Cost} onChange={(v) => setIndustrialField("sub1Cost", v)} />
                <Field label="부자재2 이름" type="text" value={industrial.sub2Name} onChange={(v) => setIndustrialField("sub2Name", v)} />
                <Field label="부자재2 금액(원)" value={industrial.sub2Cost} onChange={(v) => setIndustrialField("sub2Cost", v)} />
                <Field label="부자재3 이름" type="text" value={industrial.sub3Name} onChange={(v) => setIndustrialField("sub3Name", v)} />
                <Field label="부자재3 금액(원)" value={industrial.sub3Cost} onChange={(v) => setIndustrialField("sub3Cost", v)} />
                <Field label="부자재4 이름" type="text" value={industrial.sub4Name} onChange={(v) => setIndustrialField("sub4Name", v)} />
                <Field label="부자재4 금액(원)" value={industrial.sub4Cost} onChange={(v) => setIndustrialField("sub4Cost", v)} />
                <Field label="부자재5 이름" type="text" value={industrial.sub5Name} onChange={(v) => setIndustrialField("sub5Name", v)} />
                <Field label="부자재5 금액(원)" value={industrial.sub5Cost} onChange={(v) => setIndustrialField("sub5Cost", v)} />
                <Field label="부자재6 이름" type="text" value={industrial.sub6Name} onChange={(v) => setIndustrialField("sub6Name", v)} />
                <Field label="부자재6 금액(원)" value={industrial.sub6Cost} onChange={(v) => setIndustrialField("sub6Cost", v)} />
              </div>
            </Card>

            <Card title="비율 설정">
              <Field label="로스(%)" value={industrial.lossRate} onChange={(v) => setIndustrialField("lossRate", v)} />
              <Field label="인건비(%)" value={industrial.laborRate} onChange={(v) => setIndustrialField("laborRate", v)} />
              <Field label="판관비(%)" value={industrial.sgnaRate} onChange={(v) => setIndustrialField("sgnaRate", v)} />
              <Field label="이자비용(%)" value={industrial.interestRate} onChange={(v) => setIndustrialField("interestRate", v)} />
              <Field label="마진(%)" value={industrial.marginRate} onChange={(v) => setIndustrialField("marginRate", v)} />
            </Card>

            <Card title="산업용 계산 결과">
              {industrialResults.separatorError && <div className="rounded-2xl bg-red-50 px-4 py-3 text-sm text-red-700">{industrialResults.separatorError}</div>}
              <Row label="여재면적" value={`${fixed(industrialResults.mediaArea, 4)} ㎡`} />
              <Row label="여재무게" value={mediaType === "GLASS" ? `${fixed(industrialResults.mediaWeight, 4)} kg` : "-"} />
              <Row label="여재원가" value={money(industrialResults.mediaCost)} />
              {filterType === "SEPARATOR" && <Row label="호일무게" value={`${fixed(industrialResults.foilWeight, 4)} kg`} />}
              {filterType === "SEPARATOR" && <Row label="호일원가" value={money(industrialResults.foilCost)} />}
              <Row label="우레탄원가" value={money(industrialResults.urethaneCost)} />
              {filterType === "MINI" && <Row label="핫멜트원가" value={money(industrialResults.hotmeltCost)} />}
              <Row label="프레임원가" value={money(industrialResults.frameCost)} />
              <Row label="부자재합" value={money(industrialResults.subTotal)} />
              <div className="my-2 h-px bg-slate-200" />
              <Row label="재료비 합계" value={money(industrialResults.materialCost)} strong />
              <Row label="로스비용" value={money(industrialResults.lossCost)} />
              <Row label="인건비" value={money(industrialResults.laborCost)} />
              <Row label="판관비" value={money(industrialResults.sgnaCost)} />
              <Row label="이자비용" value={money(industrialResults.interestCost)} />
              <Row label="총원가" value={money(industrialResults.totalCost)} strong />
              <Row label="판매가" value={money(industrialResults.sellingPrice)} strong />
            </Card>
          </>
        )}

        {productGroup === "HOME_FLAT" && (
          <>
            <Card title="가정용 평판 원가설정">
              <Field label="원단 단가 (원/㎡)" value={flat.mediaUnitCost} onChange={(v) => setFlatField("mediaUnitCost", v)} />
              <Field label="핫멜트 단가 (원/kg)" value={flat.hotmeltUnitCost} onChange={(v) => setFlatField("hotmeltUnitCost", v)} />
              <Field label="띠밴드 단가 (원/m)" value={flat.bandUnitCost} onChange={(v) => setFlatField("bandUnitCost", v)} />
              <Field label="띠밴드 폭 (mm)" value={flat.bandWidthMm} onChange={(v) => setFlatField("bandWidthMm", v)} />
            </Card>

            <Card title="가정용 평판 기본 입력">
              <Field label="가로(mm)" value={flat.width} onChange={(v) => setFlatField("width", v)} />
              <Field label="세로(mm)" value={flat.height} onChange={(v) => setFlatField("height", v)} />
              <Field label="두께(mm)" value={flat.depth} onChange={(v) => setFlatField("depth", v)} />
              <Field label="산수" value={flat.pleatCount} onChange={(v) => setFlatField("pleatCount", v)} />
              <Field label="프레임 단가(원)" value={flat.frameCost} onChange={(v) => setFlatField("frameCost", v)} />
            </Card>

            <Card title="가정용 평판 부자재">
              <Field label="탈취 금액(원)" value={flat.deodorantCost} onChange={(v) => setFlatField("deodorantCost", v)} />
              <Field label="가스켓 금액(원)" value={flat.gasketCost} onChange={(v) => setFlatField("gasketCost", v)} />
              <Field label="인쇄부직포 금액(원)" value={flat.printNonwovenCost} onChange={(v) => setFlatField("printNonwovenCost", v)} />
              <Field label="비닐 금액(원)" value={flat.vinylCost} onChange={(v) => setFlatField("vinylCost", v)} />
              <Field label="에어스루 금액(원)" value={flat.airThroughCost} onChange={(v) => setFlatField("airThroughCost", v)} />
              <Field label="박스 금액(원)" value={flat.boxCost} onChange={(v) => setFlatField("boxCost", v)} />
            </Card>

            <Card title="가정용 평판 비율 설정">
              <Field label="로스(%)" value={flat.lossRate} onChange={(v) => setFlatField("lossRate", v)} />
              <Field label="인건비(%)" value={flat.laborRate} onChange={(v) => setFlatField("laborRate", v)} />
              <Field label="판관비(%)" value={flat.sgnaRate} onChange={(v) => setFlatField("sgnaRate", v)} />
              <Field label="이자비용(%)" value={flat.interestRate} onChange={(v) => setFlatField("interestRate", v)} />
              <Field label="마진(%)" value={flat.marginRate} onChange={(v) => setFlatField("marginRate", v)} />
            </Card>

            <Card title="가정용 평판 계산 결과">
              <Row label="팩 가로" value={`${fixed(flatResults.packWidth, 0)} mm`} />
              <Row label="팩 세로" value={`${fixed(flatResults.packHeight, 0)} mm`} />
              <Row label="팩 두께" value={`${fixed(flatResults.packDepth, 0)} mm`} />
              <Row label="원단면적" value={`${fixed(flatResults.mediaArea, 4)} ㎡`} />
              <Row label="원단원가" value={money(flatResults.mediaCost)} />
              <Row label="핫멜트 라인수" value={String(flatResults.hotmeltLines)} />
              <Row label="핫멜트원가" value={money(flatResults.hotmeltCost)} />
              <Row label="띠밴드 길이" value={`${fixed(flatResults.bandLengthM, 2)} m`} />
              <Row label="띠밴드원가" value={money(flatResults.bandCost)} />
              <Row label="띠밴드 핫멜트 무게" value={`${fixed(flatResults.bandHotmeltWeightKg, 4)} kg`} />
              <Row label="띠밴드 핫멜트원가" value={money(flatResults.bandHotmeltCost)} />
              <Row label="기타 부자재 합" value={money(flatResults.others)} />
              <div className="my-2 h-px bg-slate-200" />
              <Row label="재료비 합계" value={money(flatResults.materialCost)} strong />
              <Row label="로스비용" value={money(flatResults.lossCost)} />
              <Row label="인건비" value={money(flatResults.laborCost)} />
              <Row label="판관비" value={money(flatResults.sgnaCost)} />
              <Row label="이자비용" value={money(flatResults.interestCost)} />
              <Row label="총원가" value={money(flatResults.totalCost)} strong />
              <Row label="판매가" value={money(flatResults.sellingPrice)} strong />
            </Card>
          </>
        )}

        {productGroup === "HOME_CYL" && (
          <>
            <Card title="가정용 원형 원가설정">
              <Field label="원단 단가 (원/㎡)" value={cyl.mediaUnitCost} onChange={(v) => setCylField("mediaUnitCost", v)} />
              <Field label="핫멜트 단가 (원/kg)" value={cyl.hotmeltUnitCost} onChange={(v) => setCylField("hotmeltUnitCost", v)} />
            </Card>

            <Card title="가정용 원형 기본 입력">
              <Field label="팩 가로(mm)" value={cyl.width} onChange={(v) => setCylField("width", v)} />
              <Field label="팩 세로(mm)" value={cyl.height} onChange={(v) => setCylField("height", v)} />
              <Field label="팩 두께(mm)" value={cyl.depth} onChange={(v) => setCylField("depth", v)} />
              <Field label="산수" value={cyl.pleatCount} onChange={(v) => setCylField("pleatCount", v)} />
            </Card>

            <Card title="가정용 원형 부자재">
              <Field label="가스켓 금액(원)" value={cyl.gasketCost} onChange={(v) => setCylField("gasketCost", v)} />
              <Field label="종이허니컴 금액(원)" value={cyl.honeycombCost} onChange={(v) => setCylField("honeycombCost", v)} />
              <Field label="카본부직포 금액(원)" value={cyl.carbonNonwovenCost} onChange={(v) => setCylField("carbonNonwovenCost", v)} />
              <Field label="망 금액(원)" value={cyl.meshCost} onChange={(v) => setCylField("meshCost", v)} />
              <Field label="캡 금액(원)" value={cyl.capCost} onChange={(v) => setCylField("capCost", v)} />
              <Field label="에어스루 금액(원)" value={cyl.airThroughCost} onChange={(v) => setCylField("airThroughCost", v)} />
              <Field label="비닐 금액(원)" value={cyl.vinylCost} onChange={(v) => setCylField("vinylCost", v)} />
              <Field label="박스 금액(원)" value={cyl.boxCost} onChange={(v) => setCylField("boxCost", v)} />
            </Card>

            <Card title="가정용 원형 비율 설정">
              <Field label="로스(%)" value={cyl.lossRate} onChange={(v) => setCylField("lossRate", v)} />
              <Field label="인건비(%)" value={cyl.laborRate} onChange={(v) => setCylField("laborRate", v)} />
              <Field label="판관비(%)" value={cyl.sgnaRate} onChange={(v) => setCylField("sgnaRate", v)} />
              <Field label="이자비용(%)" value={cyl.interestRate} onChange={(v) => setCylField("interestRate", v)} />
              <Field label="마진(%)" value={cyl.marginRate} onChange={(v) => setCylField("marginRate", v)} />
            </Card>

            <Card title="가정용 원형 계산 결과">
              <Row label="원단면적" value={`${fixed(cylResults.mediaArea, 4)} ㎡`} />
              <Row label="원단원가" value={money(cylResults.mediaCost)} />
              <Row label="핫멜트 라인수" value={String(cylResults.hotmeltLines)} />
              <Row label="핫멜트원가" value={money(cylResults.hotmeltCost)} />
              <Row label="기타 부자재 합" value={money(cylResults.others)} />
              <div className="my-2 h-px bg-slate-200" />
              <Row label="재료비 합계" value={money(cylResults.materialCost)} strong />
              <Row label="로스비용" value={money(cylResults.lossCost)} />
              <Row label="인건비" value={money(cylResults.laborCost)} />
              <Row label="판관비" value={money(cylResults.sgnaCost)} />
              <Row label="이자비용" value={money(cylResults.interestCost)} />
              <Row label="총원가" value={money(cylResults.totalCost)} strong />
              <Row label="판매가" value={money(cylResults.sellingPrice)} strong />
            </Card>
          </>
        )}
      </div>
    </div>
  );
}
