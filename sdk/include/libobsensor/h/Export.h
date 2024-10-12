#ifndef OB_EXPORT_H
#define OB_EXPORT_H

#ifdef OB_STATIC_DEFINE
#define OB_EXPORT
#define OB_NO_EXPORT
#else
#ifndef OB_EXPORT
#ifdef _WIN32
#ifdef OrbbecSDK_EXPORTS
/* We are building this library on Windows */
#define OB_EXPORT __declspec(dllexport)
#else
/* We are using this library on Windows */
#define OB_EXPORT __declspec(dllimport)
#endif
#else
/* We are building/using this library on Linux (or other Unix-like systems) */
#define OB_EXPORT __attribute__((visibility("default")))
#endif
#endif

#ifndef OB_NO_EXPORT
#ifdef _WIN32
#define OB_NO_EXPORT
#else
#define OB_NO_EXPORT __attribute__((visibility("hidden")))
#endif
#endif
#endif

#ifndef OB_DEPRECATED
#ifdef _WIN32
#define OB_DEPRECATED __declspec(deprecated)
#else
#define OB_DEPRECATED __attribute__((deprecated))
#endif
#endif

#ifndef OB_DEPRECATED_EXPORT
#define OB_DEPRECATED_EXPORT OB_EXPORT OB_DEPRECATED
#endif

#ifndef OB_DEPRECATED_NO_EXPORT
#define OB_DEPRECATED_NO_EXPORT OB_NO_EXPORT OB_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#ifndef OB_NO_DEPRECATED
#define OB_NO_DEPRECATED
#endif
#endif

#endif /* OB_EXPORT_H */
