; ModuleID = '../../benchmarks/fib.cpp'
source_filename = "../../benchmarks/fib.cpp"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline optnone uwtable
define dso_local i64 @_Z1fl(i64) #0 {
  %2 = alloca i64, align 8
  %3 = alloca i64, align 8
  store i64 %0, i64* %3, align 8
  %4 = load i64, i64* %3, align 8
  %5 = icmp eq i64 %4, 1
  br i1 %5, label %6, label %7

; <label>:6:                                      ; preds = %1
  store i64 1, i64* %2, align 8
  br label %19

; <label>:7:                                      ; preds = %1
  %8 = load i64, i64* %3, align 8
  %9 = icmp eq i64 %8, 2
  br i1 %9, label %10, label %11

; <label>:10:                                     ; preds = %7
  store i64 1, i64* %2, align 8
  br label %19

; <label>:11:                                     ; preds = %7
  %12 = load i64, i64* %3, align 8
  %13 = sub nsw i64 %12, 1
  %14 = call i64 @_Z1fl(i64 %13)
  %15 = load i64, i64* %3, align 8
  %16 = sub nsw i64 %15, 2
  %17 = call i64 @_Z1fl(i64 %16)
  %18 = add nsw i64 %14, %17
  store i64 %18, i64* %2, align 8
  br label %19

; <label>:19:                                     ; preds = %11, %10, %6
  %20 = load i64, i64* %2, align 8
  ret i64 %20
}

; Function Attrs: noinline norecurse optnone uwtable
define dso_local i32 @main() #1 {
  %1 = alloca i32, align 4
  %2 = alloca i64, align 8
  store i32 0, i32* %1, align 4
  %3 = call i64 @_Z1fl(i64 10)
  store i64 %3, i64* %2, align 8
  %4 = load i64, i64* %2, align 8
  %5 = trunc i64 %4 to i32
  ret i32 %5
}

attributes #0 = { noinline optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { noinline norecurse optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 8.0.1-+rc3-1 (tags/RELEASE_801/rc3)"}
