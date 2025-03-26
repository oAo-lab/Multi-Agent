import { reactRouter } from "@react-router/dev/vite";
import tailwindcss from "@tailwindcss/vite";
import AutoImport from 'unplugin-auto-import/vite';
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [
    tailwindcss(),
    reactRouter(),
    tsconfigPaths(),
    AutoImport({
      imports: [
        'react',
        {
          'framer-motion': ['motion'],
          react: [
            'useState',
            'useEffect',
            'useMemo',
            'useCallback',
            'useRef',
            'useContext',
            'useReducer',
            'useLayoutEffect',
            'useDebugValue',
            'useDeferredValue',
            'useTransition',
            'useId',
            'useSyncExternalStore',
            'useInsertionEffect',
          ],
        },
      ],
      dts: true,
    }),
  ],
})
