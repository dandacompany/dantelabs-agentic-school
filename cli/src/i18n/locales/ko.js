/**
 * Korean translations
 */
export default {
  // Common
  common: {
    plugins: '플러그인',
    agents: '에이전트',
    commands: '명령어',
    skills: '스킬',
    version: '버전',
    install: '설치',
    summary: '요약',
    location: '위치',
    external: '외부',
    availablePlugins: '사용 가능한 플러그인',
    yes: '예',
    no: '아니오'
  },

  // CLI descriptions
  cli: {
    description: 'Dante Labs Agentic School - Claude Code 플러그인 설치 도구',
    examples: '사용 예시',
    moreInfo: '자세한 정보',
    installAllPlugins: '# 전체 플러그인 설치',
    installSpecificPlugin: '# 특정 플러그인 설치',
    installCustomPath: '# 경로 지정 설치',
    listPlugins: '# 플러그인 목록 조회',
    showPluginInfo: '# 플러그인 상세 정보'
  },

  // Install command
  install: {
    description: '프로젝트에 플러그인 설치',
    optionPath: '설치 경로 (기본: 현재 디렉토리)',
    optionForce: '기존 파일 강제 덮어쓰기',
    optionAll: '모든 플러그인 설치',
    optionCommon: 'common 유틸리티 포함',
    optionDryRun: '실제 설치 없이 미리보기',
    optionTarget: '대상 플랫폼 (claude, gemini, antigravity, codex, opencode, openclaw, agents)',
    invalidPlatform: "잘못된 플랫폼 '{name}'. 사용 가능: {valid}",
    platformNotSupported: '{platform}은(는) {component}을(를) 지원하지 않습니다. 건너뜁니다.',
    skippedComponents: '건너뜀: 에이전트 {agents}개, 명령어 {commands}개 ({platform} 미지원)',
    platformInfo: '플랫폼: {name} ({description})',
    installTarget: '설치 대상 경로',
    loadingRegistry: '플러그인 목록 불러오는 중...',
    registryLoaded: '플러그인 목록 로드 완료',
    confirmInstallAll: '전체 {count}개 플러그인을 설치할까요?',
    installCancelled: '설치가 취소되었습니다',
    pluginNotFound: "플러그인 '{name}'을(를) 찾을 수 없습니다",
    dryRunTitle: '미리보기 - 설치 예정:',
    dryRunFooter: '--dry-run 없이 실행하면 설치됩니다.',
    installing: '{name} 설치 중...',
    installingComponent: '{plugin} 설치 중: {type} {name}',
    installed: '{name} 설치 완료',
    failedToInstall: '{name} 설치 실패: {error}',
    successMessage: '{count}개 플러그인 설치 완료',
    componentSummary: '에이전트 {agents}개, 명령어 {commands}개, 스킬 {skills}개',
    nextSteps: '다음 단계',
    nextStep1: '{command} 실행하여 사용 가능한 명령어 확인',
    nextStep2: '{command} 명령어 사용해보기',
    externalSkillsRequired: '필요한 외부 스킬'
  },

  // List command
  list: {
    description: '사용 가능한 플러그인 목록 조회',
    optionJson: 'JSON 형식으로 출력',
    optionVerbose: '상세 정보 표시',
    title: 'Dante Labs Agentic School - 플러그인 목록',
    summaryText: '플러그인 {plugins}개, 에이전트 {agents}개, 명령어 {commands}개, 스킬 {skills}개',
    installHint: '설치: npx dlabs install [플러그인명]'
  },

  // Info command
  info: {
    description: '플러그인 상세 정보 조회',
    optionJson: 'JSON 형식으로 출력',
    pluginNotFound: "플러그인 '{name}'을(를) 찾을 수 없습니다",
    agents: '에이전트',
    commands: '명령어',
    skills: '스킬',
    externalSkillsRequired: '필요한 외부 스킬',
    installHint: '설치 명령어'
  },

  // Uninstall command
  uninstall: {
    description: '프로젝트에서 플러그인 제거',
    optionPath: '프로젝트 경로 (기본: 현재 디렉토리)',
    optionYes: '확인 프롬프트 건너뛰기',
    optionTarget: '대상 플랫폼 (claude, gemini, antigravity, codex, opencode, openclaw, agents)',
    noTargetDir: '{path}에 {dir} 디렉토리가 없습니다',
    noClaudeDir: '{path}에 .claude 디렉토리가 없습니다',
    loadingRegistry: '플러그인 목록 불러오는 중...',
    pluginNotFound: "플러그인 '{name}'이(가) 레지스트리에 없습니다",
    willRemove: '{name} 제거 예정:',
    confirmUninstall: '{name}을(를) 정말 삭제하시겠습니까?',
    uninstallCancelled: '삭제가 취소되었습니다',
    uninstalling: '{name} 삭제 중...',
    uninstalled: '{name} 삭제 완료',
    removedSummary: '삭제됨: 에이전트 {agents}개, 명령어 {commands}개, 스킬 {skills}개'
  },

  // Sample command
  sample: {
    description: '학습용 샘플 파일 다운로드',
    optionAll: '모든 샘플 다운로드',
    optionList: '사용 가능한 샘플 목록',
    optionPath: '다운로드 경로 (기본: 현재 디렉토리)',
    optionForce: '기존 파일 강제 덮어쓰기',
    fetchingList: '샘플 목록 불러오는 중...',
    availableTitle: '사용 가능한 샘플',
    noSamples: '사용 가능한 샘플이 없습니다',
    downloadHint: '다운로드: npx dlabs sample <이름>',
    downloadAllHint: '전체 다운로드: npx dlabs sample --all',
    downloadingAll: '전체 {count}개 샘플 다운로드 중...',
    downloading: '{name} 다운로드 중...',
    downloadingFile: '{name} 다운로드 중: {file}',
    downloadedFiles: '{name} 다운로드 완료 ({count}개 파일)',
    downloadFailed: '{name} 다운로드 실패',
    allComplete: '전체 샘플 다운로드 완료 (총 {count}개 파일)',
    savedTo: '저장 위치: {path}',
    alreadyExists: '{name} 건너뜀 (이미 존재함, --force로 덮어쓰기 가능)',
    alreadyExistsError: '디렉토리가 이미 존재합니다: {path}',
    useForceHint: '기존 파일을 덮어쓰려면 --force 옵션을 사용하세요',
    notFound: "샘플 '{name}'을(를) 찾을 수 없습니다",
    fetchError: '샘플 목록을 불러오는 데 실패했습니다'
  },

  // Interactive installer
  interactive: {
    selectPlatform: '설치할 플랫폼을 선택하세요',
    global: '[전역]',
    selectScope: '설치 범위를 선택하세요',
    scopeProject: '프로젝트 (현재 디렉토리)',
    scopeGlobal: '전역 (홈 디렉토리)',
    scopeCustom: '사용자 지정 경로',
    enterCustomPath: '설치 경로를 입력하세요:',
    pathNotFound: '경로를 찾을 수 없습니다: {path}. 생성할까요?',
    selectPlugins: '설치할 플러그인을 선택하세요 (Space로 선택, Enter로 확인)',
    selectAtLeastOne: '최소 1개 플러그인을 선택해주세요',
    installed: '설치됨',
    loadingComponents: '컴포넌트 정보를 불러오는 중...',
    componentsLoaded: '컴포넌트 정보 로드 완료',
    wantComponentSelection: '일부 플러그인에 여러 컴포넌트 유형이 있습니다. 개별 컴포넌트를 선택할까요?',
    selectComponents: '{plugin}의 컴포넌트를 선택하세요',
    alreadyInstalledWarning: '다음 플러그인이 이미 설치되어 있습니다:',
    alreadyInstalled: '{name}이(가) 이미 설치되어 있습니다',
    updateAction: '이미 설치된 플러그인을 어떻게 처리할까요?',
    updateAll: '업데이트 (덮어쓰기)',
    skipInstalled: '설치된 항목 건너뛰기',
    cancelInstall: '설치 취소',
    nothingToInstall: '건너뛴 후 설치할 플러그인이 없습니다',
    includeCommon: 'common 유틸리티를 포함할까요? (첫 설치 시 권장)',
    commonAlreadyInstalled: 'common이 이미 설치되어 있습니다',
    summaryTitle: '설치 요약',
    summaryPlatform: '플랫폼',
    summaryTarget: '설치 경로',
    summaryPluginCount: '{count}개 플러그인',
    update: '업데이트',
    confirmProceed: '설치를 진행할까요?'
  },

  // Logger
  logger: {
    info: '정보',
    success: '성공',
    warn: '경고',
    error: '오류',
    debug: '디버그'
  }
};
