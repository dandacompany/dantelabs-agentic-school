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
    optionNoCommon: 'common 유틸리티 제외',
    optionDryRun: '실제 설치 없이 미리보기',
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
    installHint: '설치: npx dantelabs-agentic-school install [플러그인명]'
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

  // Logger
  logger: {
    info: '정보',
    success: '성공',
    warn: '경고',
    error: '오류',
    debug: '디버그'
  }
};
